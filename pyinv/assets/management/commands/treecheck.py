from assets.models import Location
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Check the asset and location tree'  # noqa: A003

    def _check_empty_location(self, location: Location) -> None:
        """
        Check if the location is empty.

        If it is, delete it!
        """
        # We need to check for None here, in case it was previously deleted in a cleanup.
        if location and location.contents.count() == 0 and location.children_set.count() == 0:
            self.addProblem(f"Location {location} has no assets or child locations")
            self.stdout.write(f"Autofix!: Deleting {location}")
            self._fixes += 1
            location.delete()
            self._check_empty_location(location.parent)

    def check_locations(self) -> None:
        for location in Location.objects.all():
            if location:
                # check for loop
                self.assertCondition(location.parent_id != location.id, "Location has a loop")

                # check that linked asset is valid
                if location.asset:
                    self.assertCondition(
                        location.parent is not None,
                        f"Location {location} has a linked asset but no parent",
                    )
                    self.assertCondition(
                        location.asset.location == location.parent,
                        f"Location {location} has a linked asset {location.asset} that "
                        f"is not in this location's parent {location.parent}",
                    )
                    self.assertCondition(
                        location.name is not None,
                        f"Location {location} has a linked asset but a name",
                    )

                    self.assertCondition(
                        location.asset.state == "K",
                        f"Location {location} has a linked asset {location.asset} that is not in a known state",
                    )
                    self.assertCondition(
                        location.asset.asset_model.is_container,
                        f"Location {location} has a linked asset {location.asset} that is not a container",
                    )
                else:
                    self.assertCondition(
                        location.name is not None,
                        f"Location {location} has no linked asset and no name",
                    )

                # Check for and remove empty locations
                self._check_empty_location(location)

    def assertCondition(self, condition: bool, message: str) -> None:
        if not condition:
            self.addProblem(message)

    def addProblem(self, message: str) -> None:
        self._problems += 1
        self.stderr.write(message)

    def handle(self, *args, **options):
        self._problems = 0
        self._fixes = 0

        self.check_locations()

        self.stderr.write(f"{self._problems} problems found")
        self.stderr.write(f"{self._fixes} fixes applied")
