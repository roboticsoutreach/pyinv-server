# Locations

A *location* is a place where an asset can be located.

Every asset **must** have a location, unless it is lost or disposed.

A location can optionally have a parent location. If it does not have a parent location, it appears in the root of the location tree.

A location **must** contain at least one other location, or at least one asset. Otherwise, the location **must** be deleted.

## Linked Assets

A location can also be linked to an asset, which represents that the location *is the asset*, i.e the contents of the location are within the asset.

If a location is linked to an asset, it must have a parent location. This is because every asset must have a location.

The linked asset must also be in a *KNOWN* state and the linked asset's model must have `is_container` set to `true`.

## Location Operations

This section details what steps and checks need to be made to satify the constraints during operations on a location.

### Creating a location

When creating a location, the following steps need to be taken:

- If the location will be linked to an asset:
  - Require a parent location.
  - Check the asset is in the location of the desired parent.
  - Check that the asset can be a container
  - Check that the asset is in a *KNOWN* state
  - Check that the asset is not already linked to a location.
- Create a location object and set the parent if necessary.

### Moving a location

If the location is linked to an asset, refer to the section on moving an asset with a linked location.

Otherwise, you must create a new location. The old location should be deleted when it is empty.