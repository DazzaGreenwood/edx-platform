"""
Integration tests for importing courses containing pure XBlocks.
"""

from django.test.utils import override_settings

from xblock.core import XBlock
from xblock.fields import String

from xmodule.modulestore.xml_importer import import_from_xml
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.django import modulestore
from contentstore.tests.modulestore_config import TEST_MODULESTORE


class StubXBlock(XBlock):
    """
    Stub XBlock to use in tests.

    The default XBlock implementation will load this XBlock
    from XML, using the lowercase version of the class
    as an element name ("stubxblock") and the field names
    as attributes of that element.

    Example:
        <stubxblock test_field="this is only a test" />
    """
    test_field = String(default="default")


@override_settings(MODULESTORE=TEST_MODULESTORE)
class XBlockImportTest(ModuleStoreTestCase):

    def setUp(self):
        self.store = modulestore('direct')
        self.draft_store = modulestore('default')

    @XBlock.register_temp_plugin(StubXBlock)
    def test_import_public(self):
        self._assert_import(
            'pure_xblock_public',
            'i4x://edX/pure_xblock_public/stubxblock/xblock_test',
            'set by xml'
        )

    @XBlock.register_temp_plugin(StubXBlock)
    def test_import_draft(self):
        self._assert_import(
            'pure_xblock_draft',
            'i4x://edX/pure_xblock_draft/stubxblock/xblock_test@draft',
            'set by xml',
            has_draft=True
        )

    def _assert_import(self, course_dir, expected_xblock_loc, expected_field_val, has_draft=False):
        """
        Import a course from XML, then verify that the XBlock was loaded
        with the correct field value.

        Args:
            course_dir (str): The name of the course directory (relative to the test data directory)
            expected_xblock_loc (str): The location of the XBlock in the course.
            expected_field_val (str): The expected value of the XBlock's test field.

        Kwargs:
            has_draft (bool): If true, check that a draft of the XBlock exists with
                the expected field value set.

        """
        import_from_xml(
            self.store, 'common/test/data', [course_dir],
            draft_store=self.draft_store
        )

        xblock = self.store.get_item(expected_xblock_loc)
        self.assertTrue(isinstance(xblock, StubXBlock))
        self.assertEqual(xblock.test_field, expected_field_val)

        if has_draft:
            draft_xblock = self.draft_store.get_item(expected_xblock_loc)
            self.assertTrue(isinstance(draft_xblock, StubXBlock))
            self.assertEqual(draft_xblock.test_field, expected_field_val)
