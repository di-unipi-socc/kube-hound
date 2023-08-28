resource "alicloud_db_instance" "pass" {
  engine              = "MySQL"
  engine_version      = "5.6"
  instance_type   = "rds.mysql.t1.small"
  instance_storage = "10"
  parameters = [{
    name  = "innodb_large_prefix"
    value = "ON"
    }, {
    name  = "connect_timeout"
    value = "50"
  }]
}