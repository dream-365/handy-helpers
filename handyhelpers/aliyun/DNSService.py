from .ApiUtils import ApiUtils
from .ClientProvider import ClientProvider
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest

class DomainRecord:
    def __init__(self, record_dict):
        self.status = record_dict.get("Status")
        self.rr = record_dict.get("RR")
        self.line = record_dict.get("Line")
        self.locked = record_dict.get("Locked")
        self.type = record_dict.get("Type")
        self.domain_name = record_dict.get("DomainName")
        self.value = record_dict.get("Value")
        self.record_id = record_dict.get("RecordId")
        self.update_timestamp = record_dict.get("UpdateTimestamp")
        self.ttl = record_dict.get("TTL")
        self.create_timestamp = record_dict.get("CreateTimestamp")
        self.weight = record_dict.get("Weight")

    def __repr__(self):
        return (f"DomainRecord(status={self.status}, rr={self.rr}, line={self.line}, "
                f"locked={self.locked}, type={self.type}, domain_name={self.domain_name}, "
                f"value={self.value}, record_id={self.record_id}, update_timestamp={self.update_timestamp}, "
                f"ttl={self.ttl}, create_timestamp={self.create_timestamp}, weight={self.weight})")


class DNSService:
    def __init__(self):
        self.region_id = 'cn-hangzhou'
        pass

    def describeDomainRecords(self, domain_name, rr_name):
        client = ClientProvider.getClient(self.region_id)
        request = DescribeDomainRecordsRequest()
        request.set_DomainName(domain_name)
        request.set_RRKeyWord(rr_name)
        api_response = ApiUtils.perform_request(client, request)
        return DNSService._parse_domain_records_from_api_response(api_response)
    
    def getFirstDomainRecord(self, domain_name, rr_name):
        records = self.describeDomainRecords(domain_name, rr_name)
        return records[0] if records else None

    def updateDNSRecordValue(self, domain_name, rr_name, new_value):
        client = ClientProvider.getClient(self.region_id)
        record = self.getFirstDomainRecord(domain_name, rr_name)
        request = UpdateDomainRecordRequest()
        request.set_RecordId(record.record_id)
        request.set_RR(record.rr)
        request.set_Type(record.type)
        request.set_Value(new_value)
        ApiUtils.perform_request(client, request)

    @staticmethod
    def _parse_domain_records_from_api_response(api_response):
        """Parses domain records from the API response and returns a list of DomainRecord objects."""
        domain_records = []
        records = api_response.get("DomainRecords", {}).get("Record", [])
        for record_dict in records:
            domain_record = DomainRecord(record_dict)
            domain_records.append(domain_record)
        return domain_records