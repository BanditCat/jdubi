```bash
Usage: crypto.py [OPTIONS]

  Encrypts/decrypts using latin squares. If run without a command line, it
  will encrypt the file dec saving it as enc, or decrypt enc saving it as
  dec, depending on the presence of these files. If there is a file named
  key, it will be used as the password.

Options:
  -t, --test / --no-test     Run tests from
                             https://eprint.iacr.org/2005/352.pdf, 00103 and
                             03202 should be displayed.
  -d, --decrypt / --encrypt  Decrypt rather than encrypt. Encryption is the
                             default.
  -pw, --password-file TEXT  Password file.
  -i, --input-file TEXT      Input file.
  -o, --output-file TEXT     Output file.
  --help                     Show this message and exit.
