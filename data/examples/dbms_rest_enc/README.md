# Test Data at rest encryption in DBMS
for testing there are terraform configuration files that contain different dbms implementations

## How Test
by running the following command:

```
$ ./data/examples/dbms_rest_enc/run.sh

...
...

Analysis results:
Data-at-Rest Encryption Not Enabled in DBMSs - detected smells {NEDE}
        Description: Ensure Transparent Data Encryption is Enabled on instance 
        File type: terraform 
        File: /alibaba_cloud.tf:1-13

Data-at-Rest Encryption Not Enabled in DBMSs - detected smells {NEDE}
        Description: Ensure MongoDB has Transparent Data Encryption Enabled 
        File type: terraform 
        File: /alibaba_cloud_mongo.tf:1-10

Data-at-Rest Encryption Not Enabled in DBMSs - detected smells {NEDE}
        Description: Ensure that MySQL server enables infrastructure encryption 
        File type: terraform 
        File: /azure_mysql_server.tf:1-3
```