from django.core.management.base import BaseCommand
from django.apps import apps

## RDF Graph...
from vast_rdf.vast_repository import RDFStoreVAST

class Command(BaseCommand):
    help = 'Save all objects of all models'

    def handle(self, *args, **options):
        # Get all installed apps in the Django project
        installed_apps = apps.get_app_configs()

        for app in installed_apps:
            if app.name != 'activity_data':
                continue
            # Get all models for each app
            # models = app.get_models()
            models = (
                'Age',
                'Class',
                'ConceptType',
                'Concept',
                'DigitisationApplication',
                'Education',
                'Gender',
                'Language',
                'Nationality',
                'Nature',
                'OrganisationType',
                'Predicate',
                'ProductType',
                # The rest must be serialised in this exact order!
                'Activity',
                'Stimulus',
                'ActivityStep',
                'Context',
                'Organisation',
                'Event',
                'VisitorGroup',
                'VisitorGroupQRCode',
                'Visitor',
                'Product',
                'ProductStatement',
                'Statement',
                'QuestionnaireEntry',
                'QuestionnaireQuestion',
                'QuestionnaireAnswer',
            )
            
            rdf = RDFStoreVAST()
            for model_name in models:
                try:
                    model = app.get_model(model_name)
                    self.stdout.write(self.style.SUCCESS(f'Saving objects for model: {model.__name__}'))
                    # Call the save method for each object in the model
                    for obj in model.objects.all():
                        #obj.save()
                        rdf.save(type(obj).__name__, obj)
                    self.stdout.write(self.style.SUCCESS(f'Saved objects for model: {model.__name__}'))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error saving objects for model {model.__name__}: {e}'))
            del rdf
