import time
import requests

def calculate_speed(size: int, duration: float) -> float:
    """Calculate the speed of a download given a filesize in bytes and a duration in seconds. Returns the speed as a float in Mbps."""
    return float((size / 125000) / duration)


class Speedtest:
    # TODO write class docstring
    __DEFAULT_SMALL_URL = "http://ipv4.download.thinkbroadband.com/10MB.zip"
    __DEFAULT_MEDIUM_URL = "http://ipv4.download.thinkbroadband.com/50MB.zip"
    __DEFAULT_LARGE_URL = "http://ipv4.download.thinkbroadband.com/200MB.zip"
    
    @staticmethod
    def __run_test(url: str, verbose: bool = False) -> float:
        """Download the file at url and return a float representing the speed the file was downloaded in Mbps."""
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        duration = end_time - start_time
        if verbose:
            return (len(response.content), duration, calculate_speed(len(response.content), duration))
        return calculate_speed(len(response.content), duration)

    def __init__(self, small_url: str = None, medium_url: str = None, large_url: str = None):
        self.small_url = small_url if small_url is not None else Speedtest.__DEFAULT_SMALL_URL
        self.medium_url = medium_url if medium_url is not None else Speedtest.__DEFAULT_MEDIUM_URL
        self.large_url = large_url if large_url is not None else Speedtest.__DEFAULT_LARGE_URL
        # TODO possible validation on the provided URLs (not accessibility just format)

    def test_small(self, verbose: bool = False) -> float | tuple[int, float, float]:
        """Perform a speedtest using a small download file and return a float in Mbps."""
        return Speedtest.__run_test(self.small_url, verbose = verbose)
    def test_medium(self, verbose: bool = False) -> float | tuple[int, float, float]:
        """Perform a speedtest using a medium download file and return a float in Mbps."""
        return Speedtest.__run_test(self.medium_url, verbose = verbose)
    def test_large(self, verbose: bool = False) -> float | tuple[int, float, float]:
        """Perform a speedtest using a large download file and return a float in Mbps."""
        return Speedtest.__run_test(self.large_url, verbose = verbose)
    



