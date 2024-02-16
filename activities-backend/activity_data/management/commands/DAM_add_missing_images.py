from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from django.db.models import Q

## RDF Graph...
from vast_rdf.vast_repository import RDFStoreVAST
## DAM Store...
from vast_rdf.vast_dam import DAMStoreVAST

class Command(BaseCommand):
    help = 'Save all missing images in DAM'

    def handle(self, *args, **options):
        # Get all installed apps in the Django project
        installed_apps = apps.get_app_configs()
        host = "https://digitisation.vast-project.eu"

        for app in installed_apps:
            if app.name != 'activity_data':
                continue
            # Get all models for each app
            # models = app.get_models()
            models = (
                'Stimulus',
                'Product',
            )

            rdf = RDFStoreVAST()
            dam = DAMStoreVAST()
            for model_name in models:
                try:
                    model = app.get_model(model_name)
                    self.stdout.write(self.style.SUCCESS(f'Processing objects for model: {model.__name__}'))
                    # Call the save method for each object in the model
                    for obj in model.objects.filter(~(Q(image=None)|Q(image=''))).filter(Q(image_resource_id=None) | Q(image_uriref=None) | Q(image_uriref='')):
                        print(obj, obj.pk, obj.product_type, host + obj.image.url, obj.image_resource_id, obj.image_uriref)
                        try:
                            obj.image_resource_id = dam.create_resource(obj.image.url, {
                                    'description': f'{type(obj).__name__}: {obj.name}',
                                }, artifact_type='image')
                            print(f"Image Resource: {obj.image_resource_id}")
                            json_data = dam.get_resource(obj.image_resource_id)
                            obj.image_uriref = dam.get_size(json_data)['url']
                            print(f"Image DAM URL: {obj.image_uriref}")

                            obj.save()
                        except Exception as e:
                            self.stderr.write(self.style.ERROR(f'Error processing object for model {model.__name__}: {e}'))
                        #rdf.save(type(obj).__name__, obj, commit=False)
                    #rdf.commit()
                    self.stdout.write(self.style.SUCCESS(f'Saved objects for model: {model.__name__}'))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error saving objects for model {model.__name__}: {e}'))
            del rdf
            del dam
