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
