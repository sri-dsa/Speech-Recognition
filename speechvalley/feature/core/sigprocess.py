import numpy
import math

def audio2frame(signal, frame_length, frame_step, winfunc=lambda x: numpy.ones((x,))):
    """Framing audio signal. Uses number of samples as unit.

    Args:
        signal: 1-D numpy array.
        frame_length: In this situation, frame_length = samplerate * win_length, since we
            use number of samples as unit.
        frame_step: In this situation, frame_step = samplerate * win_step,
            representing the number of samples between the start point of adjacent frames.
        winfunc: Lambda function to generate a vector with shape (x,) filled with ones.

    Returns:
        frames * win: 2-D numpy array with shape (frames_num, frame_length).
    """
    signal_length = len(signal)
    # Use round() to ensure length and step are integer, considering that we use number
    # of samples as unit.
    frame_length = int(round(frame_length))
    frame_step = int(round(frame_step))
    if signal_length <= frame_length:
        frames_num = 1
    else:
        frames_num = 1 + int(math.ceil((1.0 * signal_length - frame_length) / frame_step))
    pad_length = int((frames_num - 1) * frame_step + frame_length)
    # Padding zeros at the end of signal if pad_length > signal_length.
    zeros = numpy.zeros((pad_length - signal_length,))
    pad_signal = numpy.concatenate((signal, zeros))
    # Calculate the indices of signal for every sample in frames, shape (frames_num, frame_length)
    indices = numpy.tile(numpy.arange(0, frame_length), (frames_num, 1)) + numpy.tile(
        numpy.arange(0, frames_num * frame_step, frame_step), (frame_length, 1)).T
    indices = numpy.array(indices, dtype=numpy.int32)
    # Get signal data according to indices.
    frames = pad_signal[indices]
    win = numpy.tile(winfunc(frame_length), (frames_num, 1))
    return frames * win

def deframesignal(frames, signal_length, frame_length, frame_step, winfunc=lambda x: numpy.ones((x,))):
    """Define a function to transform each frame of the original signal, likely to remove correlation.

    Args:
        frames: Frame matrix returned by audio2frame function.
        signal_length: Signal length.
        frame_length: Frame length.
        frame_step: Frame step.
        winfunc: Apply a window function to each frame for analysis; by default, no window is applied here.

    Returns:
        Adjusted signal.
    """
    # Round the parameters
    signal_length = round(signal_length)  # Signal length
    frame_length = round(frame_length)  # Frame length
    frames_num = numpy.shape(frames)[0]  # Total number of frames
    assert numpy.shape(frames)[1] == frame_length, '"frames" matrix size is incorrect, its column number should equal frame length'  # Check frames dimension, handle exception
    indices = numpy.tile(numpy.arange(0, frame_length), (frames_num, 1)) + numpy.tile(
        numpy.arange(0, frames_num * frame_step, frame_step), (frame_length, 1)).T  # Extract time points for all frames, resulting in a matrix of shape frames_num * frame_length
    indices = numpy.array(indices, dtype=numpy.int32)
    pad_length = (frames_num - 1) * frame_step + frame_length  # Total length of flattened signal
    if signal_length <= 0:
        signal_length = pad_length
    recalc_signal = numpy.zeros((pad_length,))  # Adjusted signal
    window_correction = numpy.zeros((pad_length, 1))  # Window correlation
    win = winfunc(frame_length)
    for i in range(0, frames_num):
        window_correction[indices[i, :]] = window_correction[indices[i, :]] + win + 1e-15  # Indicates the degree of signal overlap
        recalc_signal[indices[i, :]] = recalc_signal[indices[i, :]] + frames[i, :]  # Original signal plus overlap forms the adjusted signal
    recalc_signal = recalc_signal / window_correction  # New adjusted signal equals adjusted signal divided by overlap at each point
    return recalc_signal[0:signal_length]  # Return the new adjusted signal

def spectrum_magnitude(frames, NFFT):
    """Apply FFT and calculate magnitude of the spectrum.

    Args:
        frames: 2-D frames array calculated by audio2frame(...).
        NFFT: FFT size.

    Returns:
        Magnitude of the spectrum after FFT, with shape (frames_num, NFFT).
    """
    complex_spectrum = numpy.fft.rfft(frames, NFFT)
    return numpy.absolute(complex_spectrum)

def spectrum_power(frames, NFFT):
    """Calculate power spectrum for every frame after FFT.

    Args:
        frames: 2-D frames array calculated by audio2frame(...).
        NFFT: FFT size.

    Returns:
        Power spectrum: PS = magnitude^2 / NFFT
    """
    return 1.0 / NFFT * numpy.square(spectrum_magnitude(frames, NFFT))

def log_spectrum_power(frames, NFFT, norm=1):
    """Calculate log power spectrum.

    Args:
        frames: 2-D frames array calculated by audio2frame(...).
        NFFT: FFT size.
        norm: Normalization flag.

    Returns:
        Log power spectrum.
    """
    spec_power = spectrum_power(frames, NFFT)
    # In case of calculating log0, set values in spec_power less than 1e-30 to 1e-30.
    spec_power[spec_power < 1e-30] = 1e-30
    log_spec_power = 10 * numpy.log10(spec_power)
    if norm:
        return log_spec_power - numpy.max(log_spec_power)
    else:
        return log_spec_power

def pre_emphasis(signal, coefficient=0.95):
    """Pre-emphasis.

    Args:
        signal: 1-D numpy array.
        coefficient: Coefficient for pre-emphasis. Defaulted to 0.95.

    Returns:
        Pre-emphasized signal.
    """
    return numpy.append(signal[0], signal[1:] - coefficient * signal[:-1])