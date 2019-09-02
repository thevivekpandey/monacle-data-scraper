# monacle-data-scraper

##Data stucture in mongodb:

Each document is of this type:

{
   _id: encodes time of metric + some random bits,
   ns: "AWS/EC2"/"AWS/ELB" etc,
   metric: "CPUUtilization"
   ts: timestamp
   dimName: "InstanceId"
   dimValue: "xyz"
}

AWS outputs "Unit" as well, but we will have some conventions and not store it 
explicitly.

We don't store statistics (i.e. whether it is sum or max or min etc)

##MySQL table for storing fetch configuration
client_id: int(11)
namespace: varchar(16)
metric: varchar(32)
dim_name: varchar(32)
dim_value: varchar(32)
period: int
stats: varchar(16)
deleted: int
created_at: datetime

##Sample feed in api_feed table:
{ "data": [ {"name": "Sep 1", "cpu": 88}, {"name": "Sep 2", "cpu": 82}, {"name": "Sep 3", "cpu": 84}, {"name": "Sep 4", "cpu": 90}, {"name": "Sep 5", "cpu": 91}, {"name": "Sep 6", "cpu": 86}, {"name": "Sep 7", "cpu": 48} ], "message": "CPU util of abcd machine has been significantly high on Sep7 <a
href=\"http://www.google.com\" target=\"_blank\">See more.</a>" }
