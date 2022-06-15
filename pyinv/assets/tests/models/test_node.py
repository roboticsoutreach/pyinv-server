from assets.models import Asset, AssetModel, Manufacturer, Node
from django.db import IntegrityError
from django.test import TestCase


class TestNode(TestCase):
    """Test the node model."""

    def setUp(self) -> None:
        """Set up the test."""
        self.manufacturer = Manufacturer(name="foo")
        self.manufacturer.save()
        self.asset_model = AssetModel(name="bar", manufacturer=self.manufacturer)
        self.asset_model.save()
        self.asset = Asset(asset_model=self.asset_model)
        self.asset.save()

    def testCreateRoot(self) -> None:
        """Test that we can create a node at the root."""
        node = Node.add_root(node_type="L", name="foo")
        self.assertEqual(node.name, "foo")
        self.assertEqual(node.node_type, "L")
        self.assertEqual(node.get_children().count(), 0)
        self.assertEqual(node.get_ancestors().count(), 0)

    def testCreateChild(self) -> None:
        """Test that we can create a child node."""
        root = Node.add_root(node_type="L", name="foo")
        child = root.add_child(node_type="L", name="bar")
        self.assertEqual(child.name, "bar")
        self.assertEqual(child.node_type, "L")

        self.assertEqual(child.get_children().count(), 0)
        self.assertEqual(list(child.get_ancestors().all()), [root])

        self.assertEqual(list(root.get_children().all()), [child])

    def testCreateGrandchild(self) -> None:
        """Test that we can create a grandchild node."""
        root = Node.add_root(node_type="L", name="foo")
        child = root.add_child(node_type="L", name="bar")
        grandchild = child.add_child(node_type="L", name="baz")
        self.assertEqual(grandchild.name, "baz")
        self.assertEqual(grandchild.node_type, "L")

        self.assertEqual(grandchild.get_children().count(), 0)
        self.assertEqual(list(grandchild.get_ancestors().all()), [root, child])

        self.assertEqual(list(root.get_children().all()), [child])
        self.assertEqual(list(root.get_descendants().all()), [child, grandchild])

        self.assertEqual(str(grandchild), "baz")

    def test_location_must_have_name(self) -> None:
        """Test that a location must have a name."""
        with self.assertRaises(IntegrityError):
            Node.add_root(node_type="L")

    def test_asset_must_have_info(self) -> None:
        """Test that an asset must have an asset info."""
        with self.assertRaises(IntegrityError):
            Node.add_root(node_type="A")

    def test_asset_link(self) -> None:
        """Test that we can link a node to an asset info."""
        node = Node.add_root(node_type="A", asset=self.asset)
        self.assertEqual(node.asset.asset_model, self.asset.asset_model)
        self.assertEqual(str(node), "foo bar")

    def test_asset_link_with_name(self) -> None:
        """Test that we can link a node to an asset info with a name."""
        node = Node.add_root(node_type="A", asset=self.asset, name="foobar")
        self.assertEqual(node.asset.display_name, "foobar")
        self.assertEqual(str(node), "foobar")

    def test_location_cannot_be_linked_to_asset(self) -> None:
        """Test that a location cannot be linked to an asset."""
        with self.assertRaises(IntegrityError):
            Node.add_root(node_type="L", name="foo", asset=self.asset)
