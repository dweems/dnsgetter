from __future__ import print_function


from flask import Flask, jsonify
from flask_restful import Resource, Api

import dns.resolver
import dns.query

app = Flask(__name__)
api = Api(app)

 
class dns_records(Resource):

    # Define dictionary for records
    records = {}

    def get_records(name):

        resolver = dns.resolver.Resolver()

        # Iterate over records and append arrays inside of dictionary
        for record in dns_records.records:
            try:
                
                # Check if the array selected is PTR or not
                if record is not "PTR":
                    query = resolver.query(str(name), str(record))
                    for response in query:
                        dns_records.records[record].append(str(response))

                # Check if it is specifically a PTR record (Didn't use else in the event that more records are check in the future)
                elif record is "PTR":
                    if dns_records.records['A']:
                        for ptr in dns_records.records['A']:
                            req = '.'.join(reversed(ptr.split("."))) + ".in-addr.arpa"
                            query = resolver.query(str(req), "PTR")
                            for response in query:
                                dns_records.records['PTR'].append(str(response))

            except:
                # If the record doesn't exist or doesn't resolve throw error
                dns_records.records[record].append("Record unavailble")

    def get(self, name):

        dns_records.records = {
            'SOA': [],
            'A': [],
            'NS': [],
            'MX': [],
            'TXT': [],
            'PTR': []
        }

        # Get records 
        dns_records.get_records(name)

        # Return records
        return jsonify(dns_records.records)
        


api.add_resource(dns_records, '/<string:name>')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
