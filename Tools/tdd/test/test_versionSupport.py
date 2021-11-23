from .context import versionSupport

from pathlib import Path

import unittest
from unittest.mock import patch

topNum = 3
midNum = 4
lowNum = 5
@patch('versionSupport.RelVerNums', [topNum, midNum, lowNum])
class TestVersionSupport(unittest.TestCase):

    def testVersionReleaseInit(self):
        o_relVer = versionSupport.VersionRelease()
        self.assertEqual(o_relVer.getHigh(),topNum)
        self.assertEqual(o_relVer.getMid(),midNum)
        self.assertEqual(o_relVer.getLow(),lowNum)
        self.assertEqual(o_relVer.getStrReleaseVersion(),"V3.4.5")

    def testVersionDevelopmentInit(self):
        o_devVer = versionSupport.VersionDevelopment()
        self.assertEqual(o_devVer.areValuesReaded, False)
        self.assertEqual(o_devVer.Time_UTC, "")
        self.assertEqual(o_devVer.Branch, "")
        self.assertEqual(o_devVer.DevName, "")
        self.assertEqual(o_devVer.DevEmail, "")
        self.assertEqual(o_devVer.HASH, "")

    def test_VD_verFileDoesntExists(self):
        o_devVer = versionSupport.VersionDevelopment()
        fldr = Path(__file__).parent
        self.assertEqual(o_devVer.readVersionFile(Path(fldr) / "ini_files" / "unexistingFile.txt"), False)

    def test_VD_verFileReadoutOK(self):
        o_devVer = versionSupport.VersionDevelopment()
        fldr = Path(__file__).parent
        self.assertEqual(o_devVer.readVersionFile(Path(fldr) / "ini_files" / "devVersionTest.txt"), True)
        self.assertEqual(o_devVer.areValuesReaded, True)
        self.assertEqual(o_devVer.Time_UTC, " 2021-11-23 10:27:17")
        self.assertEqual(o_devVer.Branch, " MNe_refactoring_UT")
        self.assertEqual(o_devVer.DevName, " Milan Neubert")
        self.assertEqual(o_devVer.DevEmail, " milan.neubert@siemens.com")
        self.assertEqual(o_devVer.HASH, "85a0951afb353d04fd3ef584cb663d63c61e65d1")

    def test_VD_verFilePrintHASHandShortHASH(self):
        o_devVer = versionSupport.VersionDevelopment()
        fldr = Path(__file__).parent
        self.assertEqual(o_devVer.readVersionFile(Path(fldr) / "ini_files" / "devVersionTest.txt"), True)
        self.assertEqual(o_devVer.getHash(), "85a0951afb353d04fd3ef584cb663d63c61e65d1")
        self.assertEqual(o_devVer.getShortedHash(1), "8...1")
        self.assertEqual(o_devVer.getShortedHash(2), "85...d1")
        self.assertEqual(o_devVer.getShortedHash(3), "85a...5d1")
        self.assertEqual(o_devVer.getShortedHash(4), "85a0...65d1")
        self.assertEqual(o_devVer.getShortedHash(5), "85a09...e65d1")
        self.assertEqual(o_devVer.getShortedHash(), "85a09...e65d1")
