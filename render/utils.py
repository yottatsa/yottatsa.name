import xml.dom.minidom
import html.parser as HTMLParser


class RawText(xml.dom.minidom.Text):
    def writexml(self, writer, indent='', addindent='', newl=''):
        '''
        patching minidom.Text.writexml:1087
        the original calls minidom._write_data:302
        below is a combined version of both, but without the '&' replacements and so on..

        https://stackoverflow.com/questions/38015864/python-xml-dom-minidom-please-dont-escape-my-strings
        '''
        if self.data:
            writer.write('{}{}{}'.format(indent, self.data, newl))


def fix_scripts(dom):
    # ldjson workaround
    for script in dom.getElementsByTagName("script"):
        r = RawText()
        r.ownerDocument = dom
        r.data = HTMLParser.unescape(script.childNodes[0].wholeText)
        for cn in script.childNodes:
            script.removeChild(cn)
        script.appendChild(r)


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
