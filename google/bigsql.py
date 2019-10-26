from google.cloud import bigquery
from datetime import datetime

last_t = datetime.strptime('2015-03-14 12:58:00', '%Y-%m-%d %H:%M:%S')

# Import globals
import json
with open('../consts.json') as json_file:
    consts = json.load(json_file)

# Class implementation
class BigSQL():
    # lowlevel def
    client = bigquery.Client()
    table_ref = client.dataset(consts["DATA_SET"]).table(consts["DATA_TABLE"])
    table = client.get_table(table_ref) 

    # get results
    def query(self, query_str):
        return self.client.query(query_str, location="US")

    def insert(self, lang, long, height=0.0, speed=0.0, _type=1, age=5):
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        row = [(now, lang, long, height, speed, _type, age)]
        errors = self.client.insert_rows(self.table, row)  # API request
        assert errors == []
        print("Added: {}".format(row[0]))

    def get_latest_by_animals(self, user_lang, user_long, dist=None):
        '''dist in km'''
        query_job = self.client.query("""
            CREATE TEMP FUNCTION dist(lat FLOAT64, lng FLOAT64, lat0 FLOAT64, lng0 FLOAT64)
            RETURNS FLOAT64
            LANGUAGE js AS \"\"\"
                function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
                    var R = 6371; // Radius of the earth in km
                    var dLat = deg2rad(lat2-lat1);  // deg2rad below
                    var dLon = deg2rad(lon2-lon1); 
                    var a = 
                        Math.sin(dLat/2) * Math.sin(dLat/2) +
                        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
                        Math.sin(dLon/2) * Math.sin(dLon/2)
                        ; 
                    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
                    var d = R * c; // Distance in km
                    return d;
                }

                function deg2rad(deg) {
                    return deg * (Math.PI/180)
                }
                return getDistanceFromLatLonInKm(lat, lng, lat0, lng0);
            \"\"\";
            
            select 
                t.timestamp,
                t.lang,
                t.long,
                t.type
            from (select t.*,
                    row_number() over (partition by type order by timestamp desc) as seqnum
                    from `Data.Birds` AS t
                    where dist(t.lang, t.long, %f, %f) < %f
                ) t
            where seqnum <= 1;
        """ % (user_lang, user_long, dist))
        return [_.values() for _ in query_job]

    def predict(self, start_time, end_time, pred, type=None):
        """
        pred=["daily", "monthly", "yearly"]
        """
        start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        diff = end-last_t
        
        # translate
        end = last_t
        start -= diff
        
        # perform prediction
        start_str = start.strftime("%Y-%m-%d %H:%M:%S")
        end_str = end.strftime("%Y-%m-%d %H:%M:%S")
        query_job = self.client.query("""
            SELECT 
                t1.ds as timestamp, 
                t1.%s as lang,
                t2.%s as long
            FROM 
                `Predictions.lang` t1
            JOIN `Predictions.long` t2 
            ON t1.ds = t2.ds
            WHERE
                t1.ds >= "%s" AND
                t1.ds <= "%s"
        """ % (pred, pred, start_str, end_str))
        res = [list(_.values()) for _ in query_job]
        
        # shift res
        for x in res:
            x[0] += diff

        # return res
        return res
    
    # delete specific object
    def delete_row(self):
        return None

# if __name__ == "__main__":  
    # handler = BigSQL()
    # res = handler.get_latest_by_animals(-40.44282073, -40.44282073, 0.1)
    # res = handler.predict("2018-12-31 12:00:00", "2019-12-31 12:00:00", "yearly")