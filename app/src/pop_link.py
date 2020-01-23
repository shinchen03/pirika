from app.src.define import create_tag
import pandas as pd

class PopulationLink():
    params = ["no","pop_all"]
    
    def convert(self, geometry, value, file_type):
        ''' Convert requested data to file. Use this function to proceed.
        '''
        link_df = self._to_df(geometry, value)
        if file_type == 'kml':      return self._to_kml(link_df)
        elif file_type == 'gml':    return self._to_citygml(link_df)
        else:                       raise ValueError("Unsupported file type.")

    @staticmethod
    def _get_link_visual_info(pop, thresh):
        ''' thresh: 25, 50, 75 percentile
        '''
        color = ["#FFFF0000", "#FF00FF00", "#FF00FFFF", "#FF0000FF"]
        i = 0

        for th in thresh:
            if pop < th:  
                return color[i]
            i = i + 1
        return color[-1]

    @staticmethod
    def _to_df(geometry, value):
        '''
        Convert input for population mesh
        '''
        if len(geometry) != len(value):
            raise ValueError
        empty_list = [None] * len(value)
    
        link_coordicates_list = []
        pop_all_list = value
    
        for geo in geometry:
            link_coordicates_list.append({
                'lat0':  geo[0][0],
                'long0': geo[0][1],
                'lat1':  geo[1][0],
                'long1': geo[1][1],
            })
    
        link_df = pd.DataFrame(columns=['No.', 'Link_coordinates',])
        link_df['no']      = list(range(len(value)))
        link_df['pop_all'] = pop_all_list 
        link_df['link']    = link_coordicates_list
        return link_df

    @staticmethod
    def _to_kml(link_df):
        ''' Write population links to the file as kml format.
            link_df: Input mesh dataframe
        '''
        def create_placemark(row, threshs):
            def write_coordinate(nw_se_dic):
                nw_lng = nw_se_dic['lat1']
                nw_lat = nw_se_dic['long1']
                se_lng = nw_se_dic['lat0']
                se_lat = nw_se_dic['long0']
        
                template = "{},{},0.5"
                coordinates = template.format(nw_lat, nw_lng) + " "
                coordinates += template.format(se_lat, se_lng) + " "
        
                return coordinates
            
            visual_color = PopulationLink._get_link_visual_info(row.pop_all, threshs)
            style = create_tag("Style", 2, value="<LineStyle><color>" + visual_color + "</color></LineStyle><PolyStyle><color>" + visual_color + "</color><fill>1</fill><outline>1</outline><width>10</width></PolyStyle>", single_line=True)
            coordinates = write_coordinate(row.link)
            polygon = "<Polygon><altitudeMode>relativeToGround</altitudeMode><outerBoundaryIs><LinearRing><coordinates>" + coordinates + "</coordinates></LinearRing></outerBoundaryIs></Polygon>"
            multigeometry = create_tag("MultiGeometry", 2, value=polygon, single_line=True)
            
            def create_simple_data(row):
                simpledatas = ""
                for param in PopulationLink.params:
                    value = row[param]
                    value = round(value, 5) if type(value) == float else value
                    simpledatas += create_tag("SimpleData", 4, attr={'name': param}, value=value, single_line=True) + "\n"
                return simpledatas
        
            extendeddata = create_tag("ExtendedData", 2, value=create_tag("SchemaData", 3, attr={"schemaUrl": "#pop"}, value=create_simple_data(row)))
        
            placemark = create_tag("Placemark", 1).format(style + "\n" + extendeddata + "\n" + multigeometry + "\n")
            return placemark
    
        placemarks = ""
        pop_sorted = list(link_df['pop_all'].sort_values())
        threshs = list(map(lambda div: pop_sorted[int(len(pop_sorted)*div/4)], [1,2,3]))
        for index, row in link_df.iterrows():
            placemarks += create_placemark(row, threshs) + "\n"
    
        def create_schema():
            schema = create_tag("Schema", attr={'name': 'pop', 'id': 'pop'})
            simplefields = ""
            for param in PopulationLink.params:
                attr_type = 'float' if param != 'meshcode' else 'string' 
                simplefields += create_tag("SimpleField", 1, attr={'name': param, 'type': attr_type}, value="", single_line=True) + "\n"
            return schema.format(simplefields)
    
        document = create_tag("Document", attr={'id': 'root_dic'}).format(create_schema() + "\n<Folder><name>pop</name>\n" + placemarks + "</Folder>")
        kml_str = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://earth.google.com/kml/2.0">\n' + document + '\n</kml>'
        return kml_str

    @staticmethod
    def _to_citygml(link_df):
        ''' Write population link to the file as CityGML format.
            link_df: Input mesh dataframe
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
    
        def create_population(row, index, threshs):
            def write_linearrings(nw_se_dic, indexs):
                ''' Write LinearRings
                ''' 
                def write_linearring(index, pos_list):
                    ''' Convert link's northern-west and south-east points to clockwise link tags.
                        Parent tags are also created by this function. 
                    '''
        
                    coordinates = ""
                    template = "<gml:pos>{} {}</gml:pos>"
                    for p in pos_list:
                        coordinates += template.format(p[0], p[1])
                    return "<gml:PolygonPatch gml:id=\"p" + str(index) + "\"><gml:exterior><gml:LinearRing>" + coordinates + "</gml:LinearRing></gml:exterior></gml:PolygonPatch>"
        
                y1 = nw_se_dic['lat1']
                x1 = nw_se_dic['long1']
                y0 = nw_se_dic['lat0']
                x0 = nw_se_dic['long0']
                thick_ratio = 0.1
                # calculate vertical vector for line thickness
                vx = (x1 - x0)*thick_ratio
                vy = -(y1 - y0)*thick_ratio
                coord_range['x0'] = min(coord_range['x0'], x0)
                coord_range['y0'] = min(coord_range['y0'], y0)
                coord_range['x1'] = max(coord_range['x1'], x1)
                coord_range['y1'] = max(coord_range['y1'], y1)
        
                vertices = [
                    [[x0-vx, y0-vy, 0], [x0+vx, y0+vy, 0], [x1+vx, y1+vy, 0], [x1-vx, y1-vy, 0], [x0-vx, y0-vy, 0]],
                ]
                linearrings = ""
                for i, v in zip(indexs, vertices):
                    linearrings += write_linearring(i, v)
                return linearrings
            
            visual_color = PopulationLink._get_link_visual_info(row.pop_all, threshs)
        
            indexs = [index]
            coordinates = write_linearrings(row.link, indexs)
            polygon = "<gml:Surface><gml:patches>{}</gml:patches></gml:Surface>"
            polygon = polygon.format(coordinates)
            gml_multi_surface = "<gml:srsName>"+str(index)+"</gml:srsName><gml:surfaceMember>{}</gml:surfaceMember>".format(polygon)
            
            targets = ""
            for i in indexs:
                targets += "<app:target>#p" + str(i) + "</app:target>"
            c = visual_color
            color = str(int(c[7:9], 16)/255.0) + " " + str(int(c[5:7], 16)/255.0) + " " + str(int(c[3:5], 16)/255.0)
            appearance = "<app:appearance><app:Appearance><app:surfaceDataMember><app:X3DMaterial><app:diffuseColor>" + color + "</app:diffuseColor>" + targets + "</app:X3DMaterial></app:surfaceDataMember></app:Appearance></app:appearance>"
            return "<urg:Population>" + appearance + "<urg:geometry><gml:MultiSurface>" + gml_multi_surface + "</gml:MultiSurface></urg:geometry><urg:total>" + str(int(row.pop_all)) + "</urg:total></urg:Population>"
    
        urg_populations = ""
        pop_sorted = list(link_df['pop_all'].sort_values())
        threshs = list(map(lambda div: pop_sorted[int(len(pop_sorted)*div/4)], [1,2,3]))
        for index, row in link_df.iterrows():
            urg_populations += "<core:cityObjectMember>" + create_population(row, index, threshs) + "</core:cityObjectMember>\n"
    
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
