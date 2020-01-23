from app.src.define import *
from app.src.pop_mesh import PopulationMesh
from app.src.pop_link import PopulationLink

class PASDownloader:
    """Converting json to CityGML/kml/csv(chart data).

    Usage: PASDownloader.convert(json)

    :param dictionary info: Visualization data(visualizationType, exportType, resultType, geometry, values)
    :return: raw string of CityGML/kml/csv file
    :raises ValueError: if unsupported value is specified.
    """
    @staticmethod
    def convert(info):
        if info['visualizationType'] == 'population':
            if info['resultType'] == 'mesh':
                return PopulationMesh().convert(info['geometry'], info['value'], info['exportType'])
            elif info['resultType'] == 'link':
                return PopulationLink().convert(info['geometry'], info['value'], info['exportType'])
            else:
                raise ValueError('Unsupported resultType')
        else:
            raise ValueError('Unsupported visualizationType')

# For test

# Population mesh(Increased)

#from population_inc import *
#res = PASDownloader.convert(population_inc)
#print(res)

# Population mesh(Decreased)

#from population_dec import *
#res = PASDownloader.convert(population_dec)
#print(res)

# Population link

#from link import *
#res = PASDownloader.convert(link)
#print(res)
