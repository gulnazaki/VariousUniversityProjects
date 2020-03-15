from flask import make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from werkzeug.exceptions import BadRequest, ServiceUnavailable, Forbidden as NoData
from resources.models import *
from resources.utils import limited_access, DecimalEncoder
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
import json
import io
import csv

class DataView:
    '''
    An "abstract" base class that implements
    the core functionality of all data views,
    regardless of the dataset they interact with
    '''
    def query_set_pars(self, areaname, resolution, date, month, year, prod_type, model_class):
        '''
        evaluates all dataview parameters and calculates
        necessary values using foreign keys
        '''
        # response format
        self.format_type = request.args.get('format', default='json')
        if self.format_type not in ['json', 'csv']:
            current_user.current_quota += 1
            db.session.commit()
            raise BadRequest(f'Unknown format type: {self.format_type}')
        # query parameters
        self.areaname = areaname
        self.resolution = resolution
        self.date = [year] if year is not None else month.split('-') if month is not None else date.split('-')
        self.prod_type = prod_type
        # check that area name exists in database (is valid)
        try:
            self.resolutionid = ResolutionCode.query.filter_by(ResolutionCodeText=self.resolution).first().Id
            temp = ActualTotalLoad.query.filter_by(AreaName=self.areaname).first() if model_class is None else model_class.query.filter_by(AreaName=self.areaname).first()
        except:
            raise ServiceUnavailable('Database error')
        if temp is None:
            raise NoData(f"No data found in database for area name '{self.areaname}'")
        # check that production type exists in database (is valid)
        if model_class == AggregatedGenerationPerType and self.prod_type != 'AllTypes':
            try:
                prod_type_entry = ProductionType.query.filter_by(ProductionTypeText=self.prod_type).first()
            except:
                raise ServiceUnavailable('Database error')
            if prod_type_entry is None:
                # special case here: restore user quota
                try:
                    current_user.current_quota += 1
                    db.session.commit()
                except:
                    raise ServiceUnavailable('Database error')
                raise BadRequest(f"Unknown production type: '{self.prod_type}'")
        try:
            self.areatypecode = AreaTypeCode.query.get(temp.AreaTypeCodeId).AreaTypeCodeText
            self.mapcode = MapCode.query.get(temp.MapCodeId).MapCodeText
        except:
            raise ServiceUnavailable('Database error')

    def query_get_results(self, model_class):
        '''
        executes query for each endpoint
        '''
        try:
            if model_class in [ActualTotalLoad, DayAheadTotalLoadForecast]:
                if len(self.date) == 3:
                    query = db.session.query(model_class).filter_by(AreaName=self.areaname, ResolutionCodeId=self.resolutionid, Year=self.date[0], Month=self.date[1], Day=self.date[2]).order_by(model_class.DateTime)
                if len(self.date) == 2:
                    query = db.session.query(model_class.Day, func.sum(model_class.TotalLoadValue).label('TotalLoadValue')).group_by(model_class.Day).filter_by(AreaName=self.areaname, ResolutionCodeId=self.resolutionid, Year=self.date[0], Month=self.date[1]).order_by(model_class.Day)
                if len(self.date) == 1:
                    query = db.session.query(model_class.Month, func.sum(model_class.TotalLoadValue).label('TotalLoadValue')).group_by(model_class.Month).filter_by(AreaName=self.areaname, ResolutionCodeId=self.resolutionid, Year=self.date[0]).order_by(model_class.Month)
            elif model_class == AggregatedGenerationPerType:
                if len(self.date) == 3:
                    query = db.session.query(model_class).filter_by(AreaName=self.areaname, ResolutionCodeId=self.resolutionid, Year=self.date[0], Month=self.date[1], Day=self.date[2]).order_by(model_class.DateTime)
                if len(self.date) == 2:
                    query = db.session.query(model_class.Day, func.sum(model_class.ActualGenerationOutput).label('ActualGenerationOutput'), model_class.ProductionTypeId).group_by(model_class.Day, model_class.ProductionTypeId).filter_by(AreaName=self.areaname, ResolutionCodeId=self.resolutionid, Year=self.date[0], Month=self.date[1]).order_by(model_class.Day)
                if len(self.date) == 1:
                    query = db.session.query(model_class.Month, func.sum(model_class.ActualGenerationOutput).label('ActualGenerationOutput'), model_class.ProductionTypeId).group_by(model_class.Month, model_class.ProductionTypeId).filter_by(AreaName=self.areaname, ResolutionCodeId=self.resolutionid, Year=self.date[0]).order_by(model_class.Month)
            else:
                query_a = self.query_get_results(ActualTotalLoad).subquery()
                query_f = self.query_get_results(DayAheadTotalLoadForecast).subquery()
                if len(self.date) == 3:
                    query = db.session.query(query_a.c.DateTime, query_a.c.TotalLoadValue.label('ActualTotalLoadValue'), query_f.c.TotalLoadValue.label('DayAheadTotalLoadForecastValue')).filter(query_a.c.DateTime == query_f.c.DateTime).order_by(query_a.c.DateTime)
                if len(self.date) == 2:
                    query = db.session.query(query_a.c.Day, query_a.c.TotalLoadValue.label('ActualTotalLoadValue'), query_f.c.TotalLoadValue.label('DayAheadTotalLoadForecastValue')).filter(query_a.c.Day == query_f.c.Day).order_by(query_a.c.Day)
                if len(self.date) == 1:
                    query = db.session.query(query_a.c.Month, query_a.c.TotalLoadValue.label('ActualTotalLoadValue'), query_f.c.TotalLoadValue.label('DayAheadTotalLoadForecastValue')).filter(query_a.c.Month == query_f.c.Month).order_by(query_a.c.Month)
        except:
            raise ServiceUnavailable('Database error')
        return query

    def dict_list(self, query_results, model_class):
        '''
        creates a list of dictionaries
        using query results
        '''
        dict_list = []
        for row in query_results.all():
            # entries standard for all endpoints
            dataset = 'ActualVSForecastedTotalLoad' if model_class is None else model_class.__name__
            temp_dict = {'Source': 'entso-e', 'Dataset': dataset, 'AreaName': self.areaname, 'AreaTypeCode': self.areatypecode, 'MapCode': self.mapcode, 'ResolutionCode': self.resolution, 'Year': int(self.date[0])}
            # entries dependent on aggregation unit (date, month, year)
            if len(self.date) == 3:
                temp_dict['Month'] = int(self.date[1])
                temp_dict['Day'] = int(self.date[2])
                temp_dict['DateTimeUTC'] = row.DateTime.strftime('%Y-%m-%d %H:%M:%S.%f')
                description = {ActualTotalLoad: 'ActualTotalLoadValue', AggregatedGenerationPerType: 'ActualGenerationOutputValue', DayAheadTotalLoadForecast: 'DayAheadTotalLoadForecastValue'}
            if len(self.date) == 2:
                temp_dict['Month'] = int(self.date[1])
                temp_dict['Day'] = int(row.Day)
                description = {ActualTotalLoad: 'ActualTotalLoadByDayValue', AggregatedGenerationPerType: 'ActualGenerationOutputByDayValue', DayAheadTotalLoadForecast: 'DayAheadTotalLoadForecastByDayValue'}
            if len(self.date) == 1:
                temp_dict['Month'] = int(row.Month)
                description = {ActualTotalLoad: 'ActualTotalLoadByMonthValue', AggregatedGenerationPerType: 'ActualGenerationOutputByMonthValue', DayAheadTotalLoadForecast: 'DayAheadTotalLoadForecastByMonthValue'}
            # entries dependent on dataset
            if model_class in [ActualTotalLoad, DayAheadTotalLoadForecast]:
                temp_dict[description[model_class]] = row.TotalLoadValue
            elif model_class == AggregatedGenerationPerType:
                try:
                    prodtype = ProductionType.query.get(row.ProductionTypeId).ProductionTypeText
                except:
                    raise ServiceUnavailable('Database error')
                if self.prod_type not in ['AllTypes', prodtype]:
                    continue
                temp_dict['ProductionType'] = prodtype
                temp_dict[description[model_class]] = row.ActualGenerationOutput
            else:
                temp_dict[description[DayAheadTotalLoadForecast]] = row.DayAheadTotalLoadForecastValue
                temp_dict[description[ActualTotalLoad]] = row.ActualTotalLoadValue
            # 'UpdateTimeUTC' entry is always the last one
            if len(self.date) == 3 and model_class in [ActualTotalLoad, AggregatedGenerationPerType, DayAheadTotalLoadForecast]:
                temp_dict['UpdateTimeUTC'] = row.UpdateTime.strftime('%Y-%m-%d %H:%M:%S.%f')
            dict_list.append(temp_dict)
        if len(dict_list) == 0:
            raise NoData(f'No data found in database')
        return dict_list

    def json_response(self, dict_list):
        '''
        creates json response
        using list of dictionaries
        '''
        response = make_response(json.dumps(dict_list, cls=DecimalEncoder))
        response.headers['content-type'] = 'application/json'
        return response

    def csv_response(self, dict_list):
        '''
        creates csv response
        using list of dictionaries
        '''
        si = io.StringIO()
        cw = csv.DictWriter(si, dict_list[0].keys())
        cw.writeheader()
        for row in dict_list:
            cw.writerow(row)
        response = make_response(si.getvalue())
        response.headers["Content-Disposition"] = 'attachment; filename=export.csv'
        response.headers['Content-Type'] = 'text/csv'
        return response

    @jwt_required
    @limited_access
    def response(self, areaname, resolution, date, month, year, prod_type=None, model_class=None):
        '''
        queries database and creates
        endpoint's response
        '''
        self.query_set_pars(areaname, resolution, date, month, year, prod_type, model_class)
        query_res = self.query_get_results(model_class)
        dict_list = self.dict_list(query_res, model_class)
        return self.csv_response(dict_list) if self.format_type == 'csv' else self.json_response(dict_list)

class ATL(DataView, Resource):
    '''
    Actual Total Load dataset resource
    '''
    def get(self, areaname, resolution, date=None, month=None, year=None):
        return super().response(areaname, resolution, date, month, year, model_class=ActualTotalLoad)

class AGPT(DataView, Resource):
    '''
    Aggregated Generation Per Type dataset resource
    '''
    def get(self, areaname, prod_type, resolution, date=None, month=None, year=None):
        return super().response(areaname, resolution, date, month, year, prod_type, model_class=AggregatedGenerationPerType)

class DATLF(DataView, Resource):
    '''
    Day-Ahead Total Load Forecast dataset resource
    '''
    def get(self, areaname, resolution, date=None, month=None, year=None):
        return super().response(areaname, resolution, date, month, year, model_class=DayAheadTotalLoadForecast)

class ATLvsDATLF(DataView, Resource):
    '''
    Actual Data Load vs Day-Ahead Total Load Forecast pseudo-dataset resource
    '''
    def get(self, areaname, resolution, date=None, month=None, year=None):
        return super().response(areaname, resolution, date, month, year)
