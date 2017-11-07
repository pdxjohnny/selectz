# Selectz

## Installation

```bash
git clone git@github.com:pdxjohnny/selectz -b cpp
cd selectz
autoreconf -vfi
./configure
sudo make install
```

> Compiles and installs selectz to the OS default location
> (usually `/usr/local/lib` and `/usr/local/include`)


## Usage

```cpp
#include <selectz.h>

int main(int args, char** argv) {
	printf("I'm using selectz version %s!!", SELECTZ_VERSION);
	return 0;
}
```
