# Assets

An asset must be either KNOWN, LOST, or DISPOSED.

If the asset is KNOWN, then the asset must have a location.

## Linked Location

An asset may have a linked location only if the asset is KNOWN and the asset model has `is_container` set to `true`.

The asset must be stored in the parent of the linked location.

## Asset Operations

### Creating

### Moving an Asset

- If asset has a linked_location:
   - Change the parent of the linked location
   - Change the location of the asset
- Otherwise:
    - Create a new location
    - Change the location of the asset
    - Check if the old location is empty, if so delete it

### Moving an Asset with a Linked Location

### Marking Lost or Disposed
