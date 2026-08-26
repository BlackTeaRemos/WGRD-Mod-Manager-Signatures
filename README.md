# WGRD Mod Manager signatures

The trust root for [WGRD Mod Manager](https://github.com/BlackTeaRemos/WGRD-Mod-Manager).

```
keys/<fingerprint>.json      one file per publisher
revoked/<fingerprint>.json   one file per retired key
```

## Adding your key

The manager writes files you need when you create a key

```
<your folder>/
  publisher.wgrdkey            private, never share this
  keys/<fingerprint>.json      this is what you submit
  revoked/<fingerprint>.json   keep safe, submit only to retire the key
```

1. Fork this repository.
2. Copy `keys/<fingerprint>.json` into `keys/`.
3. Open a pull request adding that one file.
4. Wait for the checks and for a maintainer to merge.

Do not rename the file.

## What a key file looks like

```json
{
  "fingerprint": "0123456789abcdef",
  "publicKey": "7c21...64 hex characters...",
  "publisher": "YourName",
  "addedAt": "2026-08-30"
}
```

## Retiring a key

Submit your `revoked/<fingerprint>.json`.
It carries a signature made by the key itself, so nobody else can retire your key, and you need no permission to retire it.

Revocation is permanent.
Once merged, every manager stops trusting that key, stops seeding its mods, and marks anything installed from it as unsigned.

## Terms

Submitting means you control the key, the name is not an impersonation, and you place the entry in the public domain.
Full terms in [CONTRIBUTING.md](CONTRIBUTING.md).
Registry content is CC0 1.0, see [LICENSE](LICENSE).
