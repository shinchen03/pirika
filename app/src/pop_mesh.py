from app.src.define import create_tag
import pandas as pd

class PopulationMesh():
    params = ["meshcode", "x_min", "x_max", "y_min", "y_max", "pop_all", "pop_male", "pop_female", "house_num"]
    
    def convert(self, geometry, value, file_type):
        ''' Convert requested data to file. Use this function to proceed.
        '''
        mesh_df = self._to_df(geometry, value)
        if file_type == 'kml':      return self._to_kml(mesh_df)
        elif file_type == 'gml':    return self._to_citygml(mesh_df)
        else:                       raise ValueError("Unsupported file type.")

    @staticmethod
    def _get_mesh_visual_info(pop):
        ''' Get mesh visualization params based on value of population
        '''
        if   pop <  1.0:     return { 'height': 100, 'color':"#FFFFFFFF" }
        elif pop < 10.0:     return { 'height': 200, 'color':"#FFE2F1FF" }
        elif pop < 20.0:     return { 'height': 400, 'color':"#FFBFE1FE" }
        elif pop < 30.0:     return { 'height': 600, 'color':"#FF9AD1FF" }
        elif pop < 40.0:     return { 'height': 800, 'color':"#FF83BAFF" }
        elif pop < 50.0:     return { 'height':1000, 'color':"#FF689FFE" }
        elif pop < 60.0:     return { 'height':1200, 'color':"#FF5881FE" }
        elif pop < 70.0:     return { 'height':1400, 'color':"#FF415FED" }
        elif pop < 80.0:     return { 'height':1600, 'color':"#FF2C04E0" }
        elif pop < 90.0:     return { 'height':1800, 'color':"#FF1A20CE" }
        else:                return { 'height':2000, 'color':"#FF0402B7" }

    @staticmethod
    def _to_df(geometry, value):
        '''
        Convert input for population mesh
        '''
        if len(geometry) != len(value):
            raise ValueError
        empty_list = [None] * len(value)
    
        meshvertice_list = []
        pop_all_list = value
    
        for geo in geometry:
            meshvertice_list.append({
                'lat0':  geo['north'],
                'long0': geo['west'],
                'lat1':  geo['south'],
                'long1': geo['east'],
            })
    
        mesh_df = pd.DataFrame(columns=['meshcode', 'meshvertice', 'pop_all', 'pop_male', 'pop_female', 'house_num'])
        mesh_df['meshcode']    = empty_list
        mesh_df['pop_all']     = pop_all_list 
        mesh_df['pop_male']    = empty_list
        mesh_df['pop_female']  = empty_list
        mesh_df['house_num']   = empty_list
        mesh_df['meshvertice'] = meshvertice_list
        return mesh_df

    @staticmethod
    def _to_kml(mesh_df):
        ''' Write a population mesh to the file as kml format.
            mesh_df: Input mesh dataframe
        '''
        def create_placemark(row, clockwise=True):
            def write_coordinate(nw_se_dic, height):
                ''' Convert mesh's northern-west and south-east points to clockwise/counter-clockwise mesh tags.
                    Parent tags are also created by this function. 
                '''
                nw_lng = nw_se_dic['lat1']
                nw_lat = nw_se_dic['long1']
                se_lng = nw_se_dic['lat0']
                se_lat = nw_se_dic['long0']
        
                template = "{},{}," + str(height)
                coordinates = template.format(nw_lat, nw_lng) + " "
                if clockwise:
                    coordinates += template.format(se_lat, nw_lng) + " "
                    coordinates += template.format(se_lat, se_lng) + " "
                    coordinates += template.format(nw_lat, se_lng) + " "
                else:
                    coordinates += template.format(nw_lat, se_lng) + " "
                    coordinates += template.format(se_lat, se_lng) + " "
                    coordinates += template.format(se_lat, nw_lng) + " "
                coordinates += template.format(nw_lat, nw_lng)
        
                return coordinates
            
            visual_info = PopulationMesh._get_mesh_visual_info(row.pop_all)
        
            style = create_tag("Style", 2, value="<LineStyle><color>" + visual_info['color'] + "</color></LineStyle><PolyStyle><color>" + visual_info['color'] + "</color><fill>1</fill><outline>1</outline></PolyStyle>", single_line=True)
            coordinates = write_coordinate(row.meshvertice, row.pop_all*50)#visual_info['height'])
            polygon = "<Polygon><extrude>1</extrude><altitudeMode>relativeToGround</altitudeMode><outerBoundaryIs><LinearRing><coordinates>" + coordinates + "</coordinates></LinearRing></outerBoundaryIs></Polygon>"
            multigeometry = create_tag("MultiGeometry", 2, value=polygon, single_line=True)
            
            def create_simple_data(row):
                simpledatas = ""
                for param in PopulationMesh.params:
                    if   param == "x_min":   value = row["meshvertice"]["long0"]
                    elif param == "x_max":   value = row["meshvertice"]["long1"]
                    elif param == "y_min":   value = row["meshvertice"]["lat1"]
                    elif param == "y_max":   value = row["meshvertice"]["lat0"]
                    else:                    value = row[param]
                    
                    value = round(value, 5) if type(value) == float else value
                    simpledatas += create_tag("SimpleData", 4, attr={'name': param}, value=value, single_line=True) + "\n"
                return simpledatas
        
            extendeddata = create_tag("ExtendedData", 2, value=create_tag("SchemaData", 3, attr={"schemaUrl": "#pop"}, value=create_simple_data(row)))
        
            placemark = create_tag("Placemark", 1).format(style + "\n" + extendeddata + "\n" + multigeometry + "\n")
            return placemark
    
        placemarks = ""
        for index, row in mesh_df.iterrows():
            placemarks += create_placemark(row) + "\n"
    
        def create_schema():
            schema = create_tag("Schema", attr={'name': 'pop', 'id': 'pop'})
            simplefields = ""
            for param in PopulationMesh.params:
                attr_type = 'float' if param != 'meshcode' else 'string' 
                simplefields += create_tag("SimpleField", 1, attr={'name': param, 'type': attr_type}, value="", single_line=True) + "\n"
            return schema.format(simplefields)
    
        document = create_tag("Document", attr={'id': 'root_dic'}).format(create_schema() + "\n<Folder><name>pop</name>\n" + placemarks + "</Folder>")
        kml_str = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://earth.google.com/kml/2.0">\n' + document + '\n</kml>'
        return kml_str

    @staticmethod
    def _to_citygml(mesh_df):
        ''' Write 125m population mesh to the file as CityGML format.
            mesh_df: Input mesh dataframe
        '''
        coord_range = {
            'x0' : 1000000,
            'y0' : 1000000,
            'x1' : -1000000,
            'y1' : -1000000,
            'z0' : 0,
            'z1' : 1
        }
        is2D = False
    
        def create_population(row, index):
            def write_linearrings(nw_se_dic, z, indexs):
                ''' Write LinearRings
                ''' 
                def write_linearring(index, pos_list):
                    ''' Convert mesh's northern-west and south-east points to clockwise mesh tags.
                        Parent tags are also created by this function. 
                    '''
        
                    coordinates = ""
                    if is2D:
                        template = "<gml:pos>{} {}</gml:pos>"
                        for p in pos_list:
                            coordinates += template.format(p[0], p[1])
                        return "<gml:PolygonPatch gml:id=\"p" + str(index) + "\"><gml:exterior><gml:LinearRing>" + coordinates + "</gml:LinearRing></gml:exterior></gml:PolygonPatch>"
                    else:
                        template = "<gml:pos>{} {} {}</gml:pos>"
                        for p in pos_list:
                            coordinates += template.format(p[0], p[1], p[2])
                        return "<gml:PolygonPatch gml:id=\"p" + str(index) + "\"><gml:exterior><gml:LinearRing>" + coordinates + "</gml:LinearRing></gml:exterior></gml:PolygonPatch>"
        
                y1 = nw_se_dic['lat1']
                x1 = nw_se_dic['long1']
                y0 = nw_se_dic['lat0']
                x0 = nw_se_dic['long0']
                coord_range['x0'] = min(coord_range['x0'], x0)
                coord_range['y0'] = min(coord_range['y0'], y0)
                coord_range['x1'] = max(coord_range['x1'], x1)
                coord_range['y1'] = max(coord_range['y1'], y1)
        
                if is2D:
                    vertices = [
                        [[x0, y0, 0], [x1, y0, 0], [x1, y1, 0], [x0, y1, 0], [x0, y0, 0]],  # 2D
                    ]
                else:
                    coord_range['z1'] = max(coord_range['z1'], z)
                    vertices = [
                        [[x0, y0, z], [x1, y0, z], [x1, y1, z], [x0, y1, z], [x0, y0, z]],  # Roof
                        [[x0, y0, 0], [x0, y1, 0], [x1, y1, 0], [x1, y0, 0], [x0, y0, 0]],  # Ground
                        [[x0, y0, 0], [x0, y0, z], [x0, y1, z], [x0, y1, 0], [x0, y0, 0]],  # Wall
                        [[x0, y0, 0], [x1, y0, 0], [x1, y0, z], [x0, y0, z], [x0, y0, 0]],  # Wall
                        [[x1, y0, 0], [x1, y1, 0], [x1, y1, z], [x1, y0, z], [x1, y0, 0]],  # Wall
                        [[x0, y1, 0], [x0, y1, z], [x1, y1, z], [x1, y1, 0], [x0, y1, 0]],  # Wall
                    ]
        
                linearrings = ""
                for i, v in zip(indexs, vertices):
                    linearrings += write_linearring(i, v)
                return linearrings
            
            visual_info = PopulationMesh._get_mesh_visual_info(row.pop_all)
            height = row.pop_all*50
        
            if is2D:
                indexs = [index]
            else:
                indexs = range(index*6, (index+1)*6)
            coordinates = write_linearrings(row.meshvertice, height, indexs)
            polygon = "<gml:Surface><gml:patches>{}</gml:patches></gml:Surface>"
            polygon = polygon.format(coordinates)
            gml_multi_surface = "<gml:srsName>"+str(index)+"</gml:srsName><gml:surfaceMember>{}</gml:surfaceMember>".format(polygon)
            
            targets = ""
            for i in indexs:
                targets += "<app:target>#p" + str(i) + "</app:target>"
            c = visual_info['color']
            color = str(int(c[7:9], 16)/255.0) + " " + str(int(c[5:7], 16)/255.0) + " " + str(int(c[3:5], 16)/255.0)
            appearance = "<app:appearance><app:Appearance><app:surfaceDataMember><app:X3DMaterial><app:diffuseColor>" + color + "</app:diffuseColor>" + targets + "</app:X3DMaterial></app:surfaceDataMember></app:Appearance></app:appearance>"
            return "<urg:Population>" + appearance + "<urg:geometry><gml:MultiSurface>" + gml_multi_surface + "</gml:MultiSurface></urg:geometry><urg:total>" + str(int(row.pop_all)) + "</urg:total></urg:Population>"
    
        urg_populations = ""
        for index, row in mesh_df.iterrows():
            urg_populations += "<core:cityObjectMember>" + create_population(row, index) + "</core:cityObjectMember>\n"
    
        citygml_str = """<?xml version="1.0" encoding="UTF-8"?>
    <core:CityModel 
    xmlns:urg="http://www.kantei.go.jp/jp/singi/tiiki/toshisaisei/itoshisaisei/iur/urg/1.0" 
    xmlns:bldg="http://www.opengis.net/citygml/building/2.0"
    xmlns:core="http://www.opengis.net/citygml/2.0" xmlns:gml="http://www.opengis.net/gml" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:app="http://www.opengis.net/citygml/appearance/2.0"
    xsi:schemaLocation="http://www.kantei.go.jp/jp/singi/tiiki/toshisaisei/itoshisaisei/iur/1.0 http://www.kantei.go.jp/jp/singi/tiiki/toshisaisei/itoshisaisei/iur/1.0/statisticalGrid.xsd">\n<gml:name>PAS Population output for 125m mesh</gml:name>\n"""
        boundary = "<gml:boundedBy><gml:Envelope srsName=\"CRS:84\"><gml:lowerCorner srsDimension=\"3\">" + str(coord_range['x0']) + " " + str(coord_range['y0']) + " " + str(coord_range['z0']) + "</gml:lowerCorner><gml:upperCorner srsDimension=\"3\">" + str(coord_range['x1']) + " " + str(coord_range['y1']) + " " + str(coord_range['z1']) + "</gml:upperCorner></gml:Envelope></gml:boundedBy>\n"
        citygml_str += boundary + urg_populations + "\n</core:CityModel>"""
        return citygml_str
