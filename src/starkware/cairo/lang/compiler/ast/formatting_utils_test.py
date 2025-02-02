from typing import List, Union

from starkware.cairo.lang.compiler.ast.formatting_utils import (
    ParticleFormattingConfig,
    ParticleList,
    particles_in_lines,
    set_one_item_per_line,
)


def run_test_particles_in_lines(
    particles, config: ParticleFormattingConfig, expected: str, expected_one_per_line: str
):
    with set_one_item_per_line(False):
        assert (
            particles_in_lines(
                particles=particles,
                config=config,
            )
            == expected
        )
    with set_one_item_per_line(True):
        assert (
            particles_in_lines(
                particles=particles,
                config=config,
            )
            == expected_one_per_line
        )


def test_particles_in_lines():
    particles: List[Union[str, ParticleList]] = [
        "start ",
        "foo ",
        "bar ",
        ParticleList(elements=["a", "b", "c", "dddd", "e", "f"], end="*"),
        " asdf",
    ]
    expected = """\
start foo
  bar
  a, b, c,
  dddd, e,
  f* asdf\
"""
    expected_one_per_line = """\
start foo
  bar
  a,
  b,
  c,
  dddd,
  e,
  f,
* asdf\
"""
    run_test_particles_in_lines(
        particles=particles,
        config=ParticleFormattingConfig(allowed_line_length=12, line_indent=2),
        expected=expected,
        expected_one_per_line=expected_one_per_line,
    )

    particles = [
        "func f(",
        ParticleList(elements=["x", "y", "z"], end=") -> ("),
        ParticleList(elements=["a", "b", "c"], end="):"),
    ]
    expected = """\
func f(
    x, y,
    z) -> (
    a, b,
    c):\
"""
    expected_one_per_line = """\
func f(
    x, y, z
) -> (
    a, b, c
):\
"""
    run_test_particles_in_lines(
        particles=particles,
        config=ParticleFormattingConfig(allowed_line_length=12, line_indent=4),
        expected=expected,
        expected_one_per_line=expected_one_per_line,
    )

    # Same particles, using one_per_line=True.
    expected = """\
func f(
    x,
    y,
    z) -> (
    a,
    b,
    c):\
"""
    assert (
        particles_in_lines(
            particles=particles,
            config=ParticleFormattingConfig(
                allowed_line_length=12, line_indent=4, one_per_line=True
            ),
        )
        == expected
    )

    # Same particles, using one_per_line=True, longer lines.
    expected = """\
func f(
    x, y, z) -> (
    a, b, c):\
"""
    assert (
        particles_in_lines(
            particles=particles,
            config=ParticleFormattingConfig(
                allowed_line_length=19, line_indent=4, one_per_line=True
            ),
        )
        == expected
    )

    particles = [
        "func f(",
        ParticleList(elements=["x", "y", "z"], end=") -> ("),
        ParticleList(elements=[], end="):"),
    ]
    expected = """\
func f(
    x, y, z) -> ():\
"""
    assert (
        particles_in_lines(
            particles=particles,
            config=ParticleFormattingConfig(allowed_line_length=19, line_indent=4),
        )
        == expected
    )


def test_linebreak_on_particle_space():
    """
    Tests line breaking when the line length is exceeded by the space in the ', ' seperator at the
    end of a particle.
    """
    particles: List[Union[str, ParticleList]] = [
        "func f(",
        ParticleList(elements=["x", "y", "z"], end=") -> ("),
        ParticleList(elements=[], end="):"),
    ]
    expected = """\
func f(
    x, y,
    z) -> (
    ):\
"""
    expected_one_per_line = """\
func f(
    x,
    y,
    z,
) -> ():\
"""
    run_test_particles_in_lines(
        particles=particles,
        config=ParticleFormattingConfig(allowed_line_length=9, line_indent=4),
        expected=expected,
        expected_one_per_line=expected_one_per_line,
    )

    run_test_particles_in_lines(
        particles=particles,
        config=ParticleFormattingConfig(allowed_line_length=10, line_indent=4),
        expected=expected,
        expected_one_per_line=expected_one_per_line,
    )

    expected = """\
func f(
    x,
    y,
    z) -> (
    ):\
"""
    run_test_particles_in_lines(
        particles=particles,
        config=ParticleFormattingConfig(allowed_line_length=8, line_indent=4),
        expected=expected,
        expected_one_per_line=expected_one_per_line,
    )
