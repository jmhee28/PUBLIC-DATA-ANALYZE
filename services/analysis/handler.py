	

import json
import sys
import asyncio

sys.path.append('/var/task/service')
# sys.path.append('/var/task/classes')
from analyzeService import *
from csvService import *
# from s3 import *

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
                                        
def analysis(event, context):
    try:
        resource = event['resource']

        if resource == "/anomal":
            result = getAnomally()
        elif resource == '/plot':
            makePlot()
            result = 'success'
        elif resource == '/graph':
            makeGraph()
            result = 'success'
        elif resource == '/group':
            data = getGroupInfo()
            result = json.dumps(data, cls=NumpyEncoder)
            response = {
            "statusCode": 200,
            "body": result
            }
            return response
        #slice
        elif resource == '/csv/dates':
            loop = asyncio.get_event_loop()
            try:
                loop.run_until_complete(sliceCsv())
            except Exception as e:
                print('slice 오류 발생:', e)
            finally:
                loop.close()
            result = 'sucess'
        response = {
            "statusCode": 200,
            "body": json.dumps(result)
        }
        return response
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': 'An error occurred: ' + str(e)
        }
        return response
