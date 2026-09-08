import inspect

import pytest

import validkit

PUBLIC_NAMES = [
    "is_valid_email",
    "luhn_check",
    "is_valid_iban",
    "is_valid_isbn13",
    "normalize_phone",
    "strip_accents",
    "mask_secret",
    "slugify",
    "clamp",
]


@pytest.mark.parametrize("name", PUBLIC_NAMES)
def test_public_name_is_importable(name):
    assert hasattr(validkit, name)
    assert callable(getattr(validkit, name))


@pytest.mark.parametrize(
    ("name", "param_names", "defaults", "return_annotation"),
    [
        ("is_valid_email", ["text"], {}, bool),
        ("luhn_check", ["digits"], {}, bool),
        ("is_valid_iban", ["text"], {}, bool),
        ("is_valid_isbn13", ["text"], {}, bool),
        ("normalize_phone", ["text", "country_code"], {}, str),
        ("strip_accents", ["text"], {}, str),
        ("mask_secret", ["text", "keep"], {"keep": 4}, str),
        ("slugify", ["text"], {}, str),
        ("clamp", ["value", "low", "high"], {}, float | int),
    ],
)
def test_signature(name, param_names, defaults, return_annotation):
    sig = inspect.signature(getattr(validkit, name))
    params = list(sig.parameters.values())
    assert [p.name for p in params] == param_names
    for pname, default in defaults.items():
        param = sig.parameters[pname]
        assert param.default == default
        assert param.default is not inspect.Parameter.empty
    for pname in param_names:
        if pname not in defaults:
            assert sig.parameters[pname].default is inspect.Parameter.empty
    assert sig.return_annotation == return_annotation


def test_all_exported_names_are_the_nine_expected():
    assert sorted(validkit.__all__) == sorted(PUBLIC_NAMES)
