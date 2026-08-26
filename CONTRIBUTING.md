# Submitting to the signature registry

This repository is the trust root for WGRD Mod Manager.
It holds one JSON file per publisher key and one JSON file per revocation.
Nothing else belongs here.

Every installation of the manager copies this registry, so its contents are public by design and are published under CC0 1.0 Universal.
See the LICENSE file.

## Terms for every submission

By opening a pull request against this repository you agree to all of the following for the files you add.

### 1. You dedicate the entry to the public domain

You waive every copyright and related right you hold in the submitted file, to the fullest extent permitted by law, under CC0 1.0 Universal.
Where a waiver is not legally possible, you grant an unconditional, irrevocable, royalty-free licence to use the file for any purpose.

### 2. You control the key

You confirm that you hold the private key corresponding to the `publicKey` field you submit, and that you generated it yourself.

Submitting a key you do not control is a violation of these terms.

### 3. The name is yours to use

You confirm that the `publisher` name does not impersonate another person, project, or organisation, and that you are not passing yourself off as an existing publisher in this registry.

### 4. Entries may be removed or revoked

The registry maintainer may refuse, remove, or mark as revoked any entry, at any time, for any reason, without notice.
Inclusion in this registry is not a guarantee, an endorsement, or a certification of anything.

### 5. No warranty

The registry is provided as is.
The maintainer makes no warranty about the identity, conduct, or software of any publisher listed here.

## What the automation checks

Continuous integration verifies structure only.
It confirms that a file name matches its fingerprint, that the fingerprint is the blake3 digest of the public key, that no public key appears twice, that a pull request adds at most one key and one revocation, and that existing files are never modified or deleted.

## Revocation

A revocation is accepted when it carries a valid signature made by the key it revokes, or when a maintainer opens the pull request.
