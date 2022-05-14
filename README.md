# PyInv 

Online Quartermaster and Inventory System.

### Planned

- Asset oriented inventory system
- Based around a hierarchical tree of assets, some of which contain others.
- Track asset models and manufacturers, including the history thereof
- Track countable items, where only the quantity and location matter
- Human-friendly Asset Code format with Damm checksum
- (WIP) REST API
- Powerful auditing engine
- Printer Support
- Report generation
- Barcode scanner support

## Deployment

PyInv requires Python 3.8 or higher.

The [Django deployment guidelines](https://docs.djangoproject.com/en/3.2/howto/deployment/) are and should be used.

You'll need to run a couple of management commands to get going:

```bash
./manage.py createsuperuser
```