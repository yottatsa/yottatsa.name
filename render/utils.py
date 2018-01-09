
def strip_pgp(text):
    PGP_SIGNED_MESSAGE = '-----BEGIN PGP SIGNED MESSAGE-----'
    PGP_SIGNATURE_BEGIN = '-----BEGIN PGP SIGNATURE-----'
    PGP_SIGNATURE_END = '-----END PGP SIGNATURE-----'

    if PGP_SIGNED_MESSAGE not in text:
        return text

    result = []

    remove_hash = False
    skip_line = False
    remove_signature = False
    signature = False

    for line in text.split('\n'):
        if line == PGP_SIGNED_MESSAGE:
            signature = True
            remove_hash = True
            continue

        if line.startswith('Hash:') and remove_hash:
            remove_hash = False
            skip_line = True
            continue

        if line == PGP_SIGNATURE_BEGIN and signature:
            remove_signature = True
            continue

        if line == PGP_SIGNATURE_END and remove_signature:
            remove_signature = False
            signature = False
            continue

        if remove_signature:
            continue

        if line == '' and skip_line:
            continue

        skip_line = False
        result.append(line)

    assert not remove_hash
    assert not skip_line
    assert not remove_signature
    assert not signature

    return '\n'.join(result)
