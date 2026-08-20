# Retransmission Daemon Docker

This repository provides an automatically updated, lightweight Docker image for Retransmission (a fork of the Transmission BitTorrent client).

## 🏷 Supported Tags

**⚠️ Note on Retransmission Releases:** 
Currently, the `retransmission` upstream repository does not have any stable releases published. Until releases are available, **only the `main` tag will be built and updated**. Once the developers publish stable or beta releases, the CI/CD pipeline will automatically detect them and generate the tags below.

The following tags are available for use:
* `main`: Built directly from the upstream `main` branch of the Retransmission repository. (Currently the primary active tag).
* `latest`: Will represent the most recent stable release of Retransmission (Pending upstream releases).
* `latest-include-beta`: Will represent the most recent release, prioritizing betas or pre-releases (Pending upstream releases).
* **Versioned Tags**: Specific release versions (e.g., `4.1.3`) will be automatically generated based on upstream releases.

**Image path example**: `ghcr.io/abubaca4/retransmission-daemon-docker:main`

## 🚀 Usage Examples
The configuration relies on environment variables and volume mounts specific to this image. The internal volumes are `/config`, `/watch`, and `/download`. The container exposes port `9091` for the Web UI and `51413` (TCP/UDP) for peer connections.

## Docker Compose
```yaml
services:
  transmission:
    image: ghcr.io/abubaca4/retransmission-daemon-docker:main
    container_name: transmission
    environment:
      - TRANSMISSION_WATCH_DIR=/watch #optional
      - TRANSMISSION_DOWNLOAD_DIR=/download #optional
      - USER= #optional, for WebUI authentication
      - PASS= #optional, for WebUI authentication
      - WHITELIST= #optional, allowed IP addresses
      - PEERPORT=51413 #optional
      - HOST_WHITELIST= #optional, for RPC host whitelist
      - UMASK= #optional
    volumes:
      - /path/to/transmission/data:/config
      - /path/to/downloads:/download #optional
      - /path/to/watch/folder:/watch #optional
    ports:
      - 9091:9091
      - 51413:51413
      - 51413:51413/udp
    restart: unless-stopped
```

## Docker CLI
```bash
docker run -d \
  --name=transmission \
  -e TRANSMISSION_WATCH_DIR=/watch `#optional` \
  -e TRANSMISSION_DOWNLOAD_DIR=/download `#optional` \
  -e USER= `#optional` \
  -e PASS= `#optional` \
  -e WHITELIST= `#optional` \
  -e PEERPORT=51413 `#optional` \
  -e HOST_WHITELIST= `#optional` \
  -e UMASK= `#optional` \
  -p 9091:9091 \
  -p 51413:51413 \
  -p 51413:51413/udp \
  -v /path/to/transmission/data:/config \
  -v /path/to/downloads:/download `#optional` \
  -v /path/to/watch/folder:/watch `#optional` \
  --restart unless-stopped \
  ghcr.io/abubaca4/retransmission-daemon-docker:main
```

**Note on Environment Variables**: The startup script natively processes `TRANSMISSION_WATCH_DIR`, `TRANSMISSION_DOWNLOAD_DIR`, `USER`, `PASS`, `WHITELIST`, `PEERPORT`, `HOST_WHITELIST`, and `UMASK` to automatically apply your preferences at runtime. Settings adjustments using `HOST_WHITELIST` and `UMASK` dynamically modify the `settings.json` file using `jq`.

## 🔄 Image Updates & Build Frequency
This repository leverages GitHub Actions to ensure images remain secure and up to date.
* **Automated Checks**: An automated workflow checks for updates every hour.
* **Upstream Tracking**: The build system calculates a revision hash combining the upstream Transmission commit SHA and the local repository hash. If these change, a new build is triggered.
* **Routine Maintenance (7-Day Rule)**: Even if the Transmission source code hasn't changed, a forced build is triggered if the existing image is older than 7 days (604,800 seconds). This guarantees that the underlying Alpine base image and third-party libraries (like `openssl`, `libcurl`, etc.) receive the latest security patches.

### [Transmission version of this repository](https://github.com/abubaca4/transmission-daemon-docker)