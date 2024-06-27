from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import os
import dotenv
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from sqlalchemy import insert
from sqlalchemy import create_engine,text,Table,select
from flask import Response
from server.classes.forecast import Forecast
import datetime

load_dotenv()
# # instantiate the app
app = Flask(__name__,static_folder='static')
app.config.from_object(__name__)
app.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PWD')}@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
db = SQLAlchemy(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import Table
from sqlalchemy import orm
from sqlalchemy.orm import reconstructor


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    __table_args__={'schema':'minrights'}

    user_id: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]

engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# sql = '''
# SELECT * from dde.wells

# '''
# df = pd.read_sql(sql, engine)
  




# # sanity check route

@app.route('/addwells',methods=['POST'])
def add_wells():
    print(request.get_json()['user_id'])

    my_engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    forecast_out = pd.DataFrame()
    well_out = pd.DataFrame(columns=['user_id','api','well_name','well_status','well_id','operator'])
    for well in request.get_json()['wells']:
        conn = my_engine.connect()
        sql = f'''
        select * from data.prod
        where well_id = '{well['well_id']}'
        '''
        my_forecast = Forecast(well, pd.read_sql(sql, conn))
        tmp_forecast = my_forecast.forecast
        tmp_forecast['well_id'] = well['well_id']
        tmp_forecast['forecast_date'] = datetime.date.today()
        forecast_out=pd.concat([forecast_out,tmp_forecast])
        well_out.loc[len(well_out)] = [request.get_json()['user_id'],well['api'],well['well_name'],well['well_status'],well['well_id'],well['operator']]
        conn.close()
    forecast_out.to_sql('well_forecast', my_engine, if_exists='append', index=False,schema='minrights')
    well_out.to_sql('wells', my_engine, if_exists='append', index=False,schema='minrights')
    my_engine.dispose()

    return 'success'

@app.route('/get_production', methods=['GET'])
def get_production():
    my_apis = request.args['apis'].splitlines()
    
    api_lst = ','.join([f"'{x}'" for x in my_apis])
    print(api_lst)
    sql = f'''
    select p.*,w.api_10 from data.prod p
    left join data.wells w
    on p.well_id = w.well_id
    where w.api_10 in ({api_lst})
    '''

    df = pd.read_sql(sql, engine)
    out_dict ={}
    for api in my_apis:
        tmp_df = df[df['api_10'].astype(str)==str(api)]
        tmpG = tmp_df[['oil','gas','prod_date']].groupby('prod_date').sum().reset_index()

        if np.sum(tmpG['oil']) == 0:
            prod_data = {
            'labels': tmpG['prod_date'].tolist(),
            'datasets': [
                {
                'label':'Gas Production',
                'data': tmpG['gas'].tolist(),
                'borderColor':'red',
                'yAxisID':'y',
                }
                ]
            }
        else:
            prod_data = {
            'labels': tmpG['prod_date'].tolist(),
            'datasets': [
                {
                'label':'Oil Production',
                'data': tmpG['oil'].tolist(),
                'borderColor':'green',
                'yAxisID':'y',
                
                },
                {
                'label':'Gas Production',
                'data': tmpG['gas'].tolist(),
                'borderColor':'red',
                'yAxisID':'y1',
                }
                
                ]
            }
        out_dict[api] = prod_data
    
    return out_dict

@app.route('/lookup_wells', methods=['GET'])
def get_wells():
    api_lst = request.args['apis']
    print(api_lst)
    print(type(api_lst))
    api_lst = request.args['apis'].splitlines()

    api_lst = ','.join([f"'{x}'" for x in api_lst])
    sql = f'''
    select * from data.wells
    where api_10 in ({api_lst})
    '''
    df = pd.read_sql(sql, engine)
    geo_out=[]

    for i,row in df.iterrows():
        # print(i)
        # sql = f'''
        # SELECT jsonb_build_object(
        #     'type',     'FeatureCollection',
        #     'features', jsonb_agg(features.feature)
        # )
        # FROM (
        # SELECT jsonb_build_object(
        #     'type',       'Feature',
        #     'geometry',   ST_AsGeoJSON(geom)::jsonb,
        #     'properties', to_jsonb(inputs) - 'gid' - 'geom'
        # ) AS feature
        # FROM (
        #     select * from shape.wells where well_id = '{row['well_id']}'
        #     ) inputs) features;
        # ''' 
        # conn = engine.connect() 
        # myjson=conn.execute(text(sql)).fetchall()[0][0]
        # conn.close()
        # engine.dispose()

        # sql = f'''
        # SELECT jsonb_build_object(
        #     'type',     'FeatureCollection',
        #     'features', jsonb_agg(features.feature)
        # )
        # FROM (
        # SELECT jsonb_build_object(
        #     'type',       'Feature',
        #     'geometry',   ST_AsGeoJSON(geom)::jsonb,
        #     'properties', to_jsonb(inputs) - 'gid' - 'geom'
        # ) AS feature
        # FROM (
        #     SELECT trs as tooltip, basin,geom FROM shape.section
        #     where trs in (select trs from data.wells where well_id = '{row['well_id']}')
        #     ) inputs) features;
        # ''' 
        # conn = engine.connect() 
        # sec_json=conn.execute(text(sql)).fetchall()[0][0]
        # conn.close()
        # engine.dispose()


        geo_out.append(
            {'api':row['api_10'],
             'well_name':row['well_name'],
             'well_status':row['well_status'],
             'operator':row['env_operator'],
             'first_prod_date':row['first_prod_date'],
             'well_id':row['well_id'],
             'state':row['state'],
             'trs':row['trs'],
             'county':row['county']}
        )
    return jsonify(geo_out)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    stmt = insert(Users).values(user_id=data['id'],first_name=data['first_name'],last_name=data['last_name'],email=data['email'])
    
    with app.app_context():
        db.session.execute(stmt)
        db.session.commit()
    return jsonify('success')


    
@app.route('/get_assets', methods=['GET'])
def get_well_table():
    print('get assets fired')
    my_well = request.args.get('api')
    user_id = request.args['user_id']
    print(my_well)
    if my_well is not None:
        my_apis = [my_well]
        api_lst = ','.join([f"'{x}'" for x in my_apis])
        sql = f'''
        select * from minrights.wells
        where user_id = '{user_id}'
        and api in ({api_lst})'''
        print(sql)
    else:
        sql = f'''
        select * from minrights.wells
        where user_id = '{user_id}'
        '''
    df = pd.read_sql(sql, engine)
    well_data = df.to_dict(orient='records')
    
    ## prod ##
    api_lst = df['api'].tolist()
    api_lst = ','.join([f"'{x}'" for x in api_lst])
    sql = f'''
    select coalesce(p.prod_date::date,f.activity_date::date)::date as activity_date,oil,gas,prod_days,gas_forecast,oil_forecast from data.prod p
    left join minrights.well_forecast f
    on p.well_id = f.well_id
    and p.prod_date::date = f.activity_date::date
    where f.well_id in (
        select well_id from minrights.wells where user_id='{user_id}'
        and api in ({api_lst})
        
        )
    and prod_date > '2020-01-01'
    '''
    # try:
    #     my_api = request.args['api']
    #     print(request.args['api'])
    # except:
    #     my_api = None
    # engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    # sql = f'''
    # SELECT * from minrights.wells
    # where user_id = '{user_id}'
    # '''
    # df = pd.read_sql(sql, engine)
    # if len(df)==0:
    #     return {'well_data':[],'prod_data':[]}
    # well_data = df.to_dict(orient='records')
    
    # engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    # if my_api is not None:
    #     sql = f'''
    #     select * from data.prod
    #     where well_id in (select well_id from dde.wells where api = '{my_api}' and user_id='{user_id}')
    #     '''
    # else:
    #     sql = f'''
    #     select * from data.prod
    #     where well_id in (select well_id from minrights.wells where user_id='{user_id}')
        
    #     '''
    df = pd.read_sql(sql, engine)
    df = df[['oil','gas','oil_forecast','gas_forecast','activity_date']].groupby('activity_date').sum().reset_index()
    df['activity_date'] = pd.to_datetime(df['activity_date']).dt.date
    df['activity_date'] = df['activity_date'].astype(str)
    if np.sum(df['oil']) == 0:
        prod_data = {
        'labels': df['activity_date'].tolist(),
        'datasets': [
            {
            'label':'Gas Production',
            'data': df['gas'].tolist(),
            'borderColor':'red',
            'yAxisID':'y',
            },
            {
                'label':'Gas Forecast',
                'data': df['gas_forecast'].tolist(),
                'borderColor':'red',
                'yAxisID':'y',
                'borderDash':[5,5],
            }
            
            
            ]
        }
    else:
        prod_data = {
        'labels': df['activity_date'].tolist(),
        'datasets': [
            {
            'label':'Oil Production',
            'data': df['oil'].tolist(),
            'borderColor':'green',
            'yAxisID':'y',
            
            },
            {
                'label':'Oil Forecast',
                'data': df['oil_forecast'].tolist(),
                'borderColor':'green',
                'yAxisID':'y',
                'borderDash':[5,5],
                },
            {
            'label':'Gas Forecast',
                'data': df['gas_forecast'].tolist(),
                'borderColor':'red',
                'yAxisID':'y1',
                'borderDash':[5,5],
                },
            {
            'label':'Gas Production',
            'data': df['gas'].tolist(),
            'borderColor':'red',
            'yAxisID':'y1',
            }
            
            
            ]
        }
    

    out_data = {'well_data':well_data,'prod_data':prod_data}
    return out_data

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


from flask import Flask, send_from_directory
import os



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
