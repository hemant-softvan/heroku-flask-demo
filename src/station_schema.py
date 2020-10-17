from marshmallow import Schema, fields, validate


# This function is used to create station schema
class CreateStationInputSchema(Schema):
    """
    /v1/createStation - POST
    """
    # the 'required' argument ensures the field exists
    latitude = fields.Decimal(required=True)
    longitude = fields.Decimal(required=True)
    altitude = fields.Float(required=True)
    creation = fields.Date(required=True)
    international = fields.Bool(required=True)
    manufacturer = fields.Str(required=True)
    country = fields.Str(required=True)
    parametersObserved = fields.Number(required=True)
    utc = fields.String(required=True, validate=validate.Length(min=3))
    wigosID = fields.Str(required=True)
    operationalStatus = fields.Str()
    realTime = fields.Boolean()
    affiliations = fields.Str()
    observationsFrequency = fields.Number()
    internationalReportingFrequency = fields.Number()
    supervisingOrganization = fields.Str()
    rowNumber = fields.Int(required=True)
    # class Meta:
    #     dateformat = '%Y-%m-%dT%H:%M:%S%z'


class UpdateWigosInputSchema(Schema):
    """
    /v1/updateWigos - POST
    """
    # the 'required' argument ensures the field exists
    wigosId1 = fields.Str(required=True)
    wigosId2 = fields.Str(required=True)
    wigosId3 = fields.Str(required=True)
    wigosId4 = fields.Str()
    name = fields.Str(required=True)
    primaryWigosId = fields.Str(required=True)
    # class Meta:
    #     dateformat = '%Y-%m-%dT%H:%M:%S%z'


create_station_schema = CreateStationInputSchema()
update_wigos_schema = UpdateWigosInputSchema()