from distutils.version import StrictVersion

def test_project_metadata():
    import circle_asset.version as v
    StrictVersion(v.VERSION)
