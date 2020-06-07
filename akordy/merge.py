import sys, os, locale, re
locale.setlocale(locale.LC_ALL, '')

init = os.path.join(os.path.dirname(sys.argv[0]), 'init.tex')


def do_filter(songlist, filtername, default=False):
    '''From a list of song filenames, filter only those which have the filter
       'filtername' specified. When the song has no filter line, use 'default'
    '''
    result = []
    for filename in songlist:
        with open(filename, 'r', encoding='utf8') as fin:
            lines = fin.read().split('\n')

        pattern = re.compile('^\s*%\s*filter:\s*(\w+,\s*)*\w+\s*$')

        has_filters = False

        for l in lines:
            if pattern.match(l):
                has_filters = True
                filters = l.split(':')[1]
                if filtername in [ x.strip() for x in filters.split(',') ]:
                    result.append(filename)
                    break

        if not has_filters and default == True:
            result.append(filename)

    return result


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



def print_help():
    helpmsg = '''
    merge.py - script to merge individual .tex songs into the songbook

    USAGE
      python3 merge.py <songdir> <outfile> [<filtername>]

    PARAMETERS
      songdir      Directory where the songs' .tex files are
      outfile      Name of the output file
      filtername   If specified, only songs with filter <filtername> set will be merged
    '''

    print(helpmsg, file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("ERROR: At least 2 arguments are required", file=sys.stderr)
        print_help()
        sys.exit(1)

    songdir=sys.argv[1]
    outfile=sys.argv[2]
    filtername = sys.argv[3] if len(sys.argv) >= 4 else None

    songlist = [ os.path.join(songdir, x) for x in os.listdir(songdir) ]
    if filtername is not None:
        songlist = do_filter(songlist, filtername)

    songlist.sort(key=locale.strxfrm)

    do_merge(songlist, outfile)
