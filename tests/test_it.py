import os
import deck2pdf
from pytest import raises
from . import (
    current_dir,
    test_dir,
)

test_slide_path = os.path.join(test_dir, 'testslide/stub.html')


def test_help():
    raises(SystemExit, deck2pdf.main, [])
    raises(SystemExit, deck2pdf.main, ['-h'])


def test_output_default():
    deck2pdf.main([test_slide_path, '-c', 'stub'])
    assert os.path.exists(os.path.join(current_dir, '.deck2pdf'))
    assert os.path.exists(os.path.join(current_dir, 'slide.pdf'))


def test_output_file_by_name():
    output_path = os.path.join(current_dir, '.deck2pdf', 'test.output')
    deck2pdf.main([test_slide_path, '-c', 'stub', '-o', output_path])
    assert os.path.exists(os.path.join(current_dir, '.deck2pdf'))
    assert os.path.exists(output_path)


def test_capture_files():
    import glob
    output_path = os.path.join(current_dir, '.deck2pdf', 'test.output')
    deck2pdf.main([test_slide_path, '-c', 'stub', '-n', '4', '-o', output_path])
    assert os.path.exists(os.path.join(current_dir, '.deck2pdf'))
    assert os.path.exists(output_path)
    assert len(glob.glob(current_dir + '/.deck2pdf/*png')) == 4
