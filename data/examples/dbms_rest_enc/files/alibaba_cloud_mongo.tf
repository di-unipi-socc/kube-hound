resource "alicloud_mongodb_instance" "pass" {
  engine_version      = "3.4"
  db_instance_class   = "dds.mongo.mid"
  db_instance_storage = 10
  vswitch_id          = alicloud_vswitch.ditch.id
  security_ip_list    = ["10.168.1.12", "100.69.7.112"]
  kms_encryption_context= {

  }
}