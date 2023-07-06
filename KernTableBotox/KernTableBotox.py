# ----------------------------------------
# imports
# ----------------------------------------

import itertools
import time

from fontTools import ttLib
import click

from . import input_helpers

# ----------------------------------------
# constants
# ----------------------------------------


TARGETS = [".otf", ".woff", ".woff2", ".ttf"]


# ----------------------------------------
# helpers
# ----------------------------------------


def extract_kern_data(f):
    gpos = f.get("GPOS")

    # sort lookups index by feature tag

    features_to_lookup_index = {}
    for fea in gpos.table.FeatureList.FeatureRecord:
        features_to_lookup_index.setdefault(fea.FeatureTag, set())
        features_to_lookup_index[fea.FeatureTag] |= set(
            fea.Feature.LookupListIndex)
    feature_to_lookup = {}
    for fea, lookup_indexes in features_to_lookup_index.iteritems():
        feature_to_lookup[fea] = []
        for i in lookup_indexes:
            feature_to_lookup[fea].append(gpos.table.LookupList.Lookup[i])

    # extract kern values

    kern = feature_to_lookup.get("kern", [])
    my_kern = {}
    for look in kern:
        for subtable in look.SubTable:

            # deal with glyph kerning
            if hasattr(subtable, "Format") and subtable.Format == 1:
                for i, pairSet in enumerate(subtable.PairSet):
                    for pairValueRecord in pairSet.PairValueRecord:
                        if pairValueRecord.Value1.XAdvance != 0:
                            my_kern[(subtable.Coverage.glyphs[i], pairValueRecord.SecondGlyph)
                                    ] = pairValueRecord.Value1.XAdvance

            # deal with group kerning
            if hasattr(subtable, "Format") and subtable.Format == 2:
                groups_1 = {}
                groups_2 = {}
                for glyph, group_index in subtable.ClassDef1.classDefs.iteritems():
                    groups_1.setdefault(group_index, []).append(glyph)
                for glyph, group_index in subtable.ClassDef2.classDefs.iteritems():
                    groups_2.setdefault(group_index, []).append(glyph)

                # index 0 class is implicit. Great.
                grouped = [g for group in groups_1.values() for g in group]
                groups_1[0] = [g for g
                               in subtable.Coverage.glyphs if g not in grouped]

                for index_1, record_1 in enumerate(subtable.Class1Record):
                    for index_2, record_2 in enumerate(record_1.Class2Record):
                        if record_2.Value1.XAdvance != 0 and groups_1.has_key(index_1) and groups_2.has_key(index_2):
                            my_kern[(tuple(groups_1[index_1]), tuple(groups_2[index_2]))
                                    ] = record_2.Value1.XAdvance

    return my_kern


def flatten_kern(kern_dict):
    flat_kern = {}
    for p, v in kern_dict.iteritems():
        if type(p[0]) is tuple:
            for flat in itertools.product(*p):
                flat_kern[flat] = v
        else:
            flat_kern[p] = v
    return flat_kern


def filter_kern(kern_dict, max_length):
    sorted_pairs = sorted(kern_dict.keys(),
                          key=lambda x: abs(kern_dict[x]), reverse=True)
    return {pair: kern_dict[pair] for pair in sorted_pairs[:max_length]}


def build_kern_table(flat_kern_dict):
    # partly based on samples from Jeremie Hornus
    # https://github.com/sansplomb/RobofontTools/blob/master/GenerateFont/GenerateFont.py

    kern_table = ttLib.newTable('kern')
    kern_table.version = 0
    kern_table.kernTables = []

    pair_list = flat_kern_dict.items()
    # 10920 is the maximum subtable len
    for subtable_data in chunk_list(pair_list, 10920):
        subtable = ttLib.tables._k_e_r_n.KernTable_format_0()
        subtable.kernTable = {}
        subtable.coverage = 1
        subtable.format = 0
        subtable.version = 0

        for p in subtable_data:
            subtable[p[0]] = p[1]

        kern_table.kernTables.append(subtable)
    return kern_table


def chunk_list(list_, chunk_length):
    for i in range(0, len(list_), chunk_length):
        yield list_[i:i + chunk_length]


# ----------------------------------------

@click.command()
@click.option('-o', '--output_dir', default=None, help='Specify a path for the output directory', type=click.Path(exists=False))
@click.option('-t', '--suffix_tag', default="_kerntable", help='Specify a tag for the output file name (default is _kerntable)', type=str)
@click.option('--no_suffix', is_flag=True, help="Save output in place")
@click.option('--subfolder/--no_subfolder', default=False, help='process subfolders recursively')
@click.argument("input_path", type=click.Path(exists=False))
def inject_kern_table(input_path, output_dir, suffix_tag, no_suffix, subfolder):
    t = time.time()
    print("Kern Table Injection")

    # walk the i,put directory
    input_dir, font_path = input_helpers.walk_input_path(input_path,
                                                         target_extentions=TARGETS,
                                                         recursive=subfolder)
    font_count = 0
    for p in font_path:

        if output_dir:
            out_path = input_helpers.output_file_to_another_folder(
                p, output_dir)
        else:
            out_path = p

        if no_suffix:
            outpath = out_path
        else:
            outpath = input_helpers.suffix_file(out_path, suffix_tag)

        f = ttLib.TTFont(p)
        my_kern = extract_kern_data(f)
        flat_kern = flatten_kern(my_kern)
        # filter_kern = filter_kern(flat_kern, KERN_TABLE_LENGTH)
        f["kern"] = build_kern_table(flat_kern)
        f.save(outpath)
        f.close()
        print("%s -> done" % p)
        font_count += 1

    print("")
    print("All done: %s font processed in %s secs" %
          (font_count, time.time() - t))
