# Self-hosted typefaces

The onboarding site serves these fonts from the same GitHub Pages origin as the
readings. No browser request is made to a font CDN.

| Site role | Files | Official source | License |
|---|---|---|---|
| Default body and interface | `IBMPlexSans-Regular.woff2`, `IBMPlexSans-Italic.woff2`, `IBMPlexSans-Bold.woff2` | [IBM Plex](https://github.com/IBM/plex) | [SIL OFL 1.1](licenses/IBM-Plex-OFL.txt) |
| Default headings | `IBMPlexSerif-Bold.woff2` | [IBM Plex](https://github.com/IBM/plex) | [SIL OFL 1.1](licenses/IBM-Plex-OFL.txt) |
| Default code | `ibm-plex-mono-normal-400-*.woff2`, `ibm-plex-mono-normal-600-*.woff2` | [IBM Plex](https://github.com/IBM/plex) | [SIL OFL 1.1](licenses/IBM-Plex-OFL.txt) |
| Alternative body and headings | `GoogleSansFlex-Latin.woff2` | [Google Fonts: Google Sans Flex](https://fonts.google.com/specimen/Google+Sans+Flex) | [SIL OFL 1.1](licenses/Google-Sans-Flex-OFL.txt) |
| Alternative code | `GoogleSansCode-Latin.woff2` | [Google Sans Code](https://github.com/googlefonts/googlesans-code) | [SIL OFL 1.1](licenses/Google-Sans-Code-OFL.txt) |

The Google Sans files are the variable-weight Latin WOFF2 subsets returned by the
official Google Fonts CSS API. The IBM Plex Mono files provide Latin and Latin
Extended subsets at weights 400 and 600. All files were retrieved by August 25,
2026. The repository keeps the corresponding licence notices beside the binaries.
