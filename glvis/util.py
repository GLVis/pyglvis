import requests

class _GlvisData(type):
    _keys = (
    "capacitor", "distance", "ex1", "ex2", "ex27", "ex3", "ex5", "ex9",
    "klein_bottle", "laghos", "mesh_explorer", "mfem_logo", "minimal_surface",
    "mobius_strip", "navier", "quad", "quadrature_1D", "quadrature_lor",
    "remhos", "shaper", "shifted", "snake"
    )

    @staticmethod
    def _get(key):
        url = f"https://github.com/GLVis/data/raw/master/streams/{key.replace('_','-')}.saved"
        response = requests.get(url)
        # success
        if response.status_code == 200:
            return response.content.decode('utf-8').rstrip("\n")
        else:
            print(f"Failed to download data from {url}")

    def __getattr__(self, key):
        if key in self._keys:
            return self._get(key)
        else:
            raise AttributeError(f"No data named {key}")

    def __dir__(self):
        return super().__dir__() + list(self._keys)

class GlvisData(metaclass=_GlvisData):
    pass
