import sys, os, locale
locale.setlocale(locale.LC_ALL, '')

init = os.path.join(os.path.dirname(sys.argv[0]), 'init.tex')


def do_merge(songlist, outfile, initfile=init):
    '''
    Merge song files specified in 'songlist' to the output file 'outfile'.
    Unless 'initfile' is None, its contents are prepended.
    '''
    with open(outfile, 'w', encoding='utf8') as fout:
        if initfile is not None:
            fout.write(open(initfile, 'r', encoding='utf8').read())

        i = 1
        for filename in songlist:
            if not filename.endswith('.tex'):
                continue
            with open(filename, 'r', encoding='utf8') as fin:
                first, rest = fin.read().strip().split('\n', 1)
                fout.write(first)
                fout.write('\\hypertarget{song-%i}{}\\label{song-%i}\n' % (i, i))
                fout.write(rest)
                fout.write('\n\n')
            i += 1
        fout.write('\n\\end{songs}\n\\end{document}\n')



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("ERROR: 2 arguments are required", file=sys.stderr)
        sys.exit(1)

    songdir=sys.argv[1]
    outfile=sys.argv[2]
    songlist = [ os.path.join(songdir, x) for x in sorted(os.listdir(songdir),key=locale.strxfrm) ]

    do_merge(songlist, outfile)
