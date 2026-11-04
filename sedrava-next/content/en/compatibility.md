## Programs and releases

Published 0.10.0 retains regression examples from 0.9. Experimental 0.11 is not a stability or automatic migration promise. Keep compiler versions pinned and preserve project sources.

## Saved data

Storage schemas are checked strictly. Invalid JSON, duplicated identities, wrong scalar types, resource overflow and incompatible schema fingerprints reject the complete restoration. Rejected originals are retained and automatic saves are blocked; they are not silently replaced with defaults. Changing fields/capacity/persistent keys can reject older data. There is no automatic migration.

Browser data is per origin/path/application identity, local and unencrypted. It may be removed by the browser/user. Resetting a live example is an explicit deletion of only that example's storage; it never clears the whole origin.

## Android updates

Keep the same application ID, signing key and increasing versionCode. A clean install is not an upgrade test. Changing the title can change a default application ID; use an explicit stable ID before distribution. Physical-device acceptance of final 0.10 APK is not documented.

[Complete compatibility contract](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/COMPATIBILITY_010.md).
