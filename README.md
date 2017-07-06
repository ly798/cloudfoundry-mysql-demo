# cloudfoundry mysql demo

A simple cloudfoundry app demo, use flask & mysql.

## Usage

config `services` in `manifest.yml`, e.g
```
  services:
   - mysql_01
```

start application
```
cf push
```

## Validate

if the app's url is `testmysql-unrocked-etamine.cloud-09.cf-app.com`, have 3 function

### index(list users)
```
curl testmysql-unrocked-etamine.cloud-09.cf-app.com
```

### add a user
```
curl testmysql-unrocked-etamine.cloud-09.cf-app.com/1/a
```

### get a user
```
curl testmysql-unrocked-etamine.cloud-09.cf-app.com/1
```
