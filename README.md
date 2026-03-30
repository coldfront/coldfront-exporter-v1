# ColdFront Exporter v1

This plugin exports data from ColdFront 1.x to yaml files that can be imported into ColdFront 2.x

## Install

```
$ uv pip install coldfront-exporter-v1
```

Next add the app to `INSTALLED_APPS` using your `local_settings.py` file:

```
INSTALLED_APPS += ["coldfront_exporter_v1"]
```

## Exporting data

Export data to YML:

```
$ COLDFRONT_CONFIG=local_settings.py uv run coldfront export_database --output /path/to/yaml/
```

Now you can import the yaml using [coldfront-initializer](https://github.com/coldfront/coldfront-initializer).

## License

Apache 2.0
