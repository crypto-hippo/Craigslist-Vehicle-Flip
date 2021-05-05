class DDFileReader(object):

    @classmethod
    def strip_lines(cls, lines):
        return list(map(lambda x: x.strip(), lines))

    @classmethod
    def read_file_lines_stripped(cls, filepath):
        f = open(filepath, 'r')
        lines = f.readlines()
        f.close()
        del f
        return cls.strip_lines(lines)

    @classmethod
    def read_sedan_identifiers(cls):
        return cls.read_file_lines_stripped("wordbanks/sedan_identifiers.txt")

    @classmethod
    def read_coupe_identifiers(cls):
        return cls.read_file_lines_stripped("wordbanks/coupe_identifiers.txt")

    @classmethod
    def read_honda_basic_series(cls):
        return cls.read_file_lines_stripped("wordbanks/honda_basic_series.txt")

    @classmethod
    def read_honda_rare_series(cls):
        return cls.read_file_lines_stripped("wordbanks/honda_rare_series.txt")

    @classmethod
    def read_honda_rare_series_extended(cls):
        return cls.read_file_lines_stripped("wordbanks/honda_rare_series_extended.txt")

    @classmethod
    def read_is_leather_terms(cls):
        return cls.read_file_lines_stripped("wordbanks/is_leather_terms.txt")

    @classmethod
    def read_is_sunroof_terms(cls):
        return cls.read_file_lines_stripped("wordbanks/is_sunroof_terms.txt")

    @classmethod
    def read_is_sunroof_wildcard_terms(cls):
        return cls.strip_lines("wordbanks/is_sunroof_wildcard_terms.txt")

    @classmethod
    def read_leather_terms_to_nullify(cls):
        return cls.read_file_lines_stripped("wordbanks/leather_terms_to_nullify.txt")

    @classmethod
    def read_leather_wildcard_terms_to_nullify(cls):
        return cls.read_file_lines_stripped("wordbanks/leather_wildcard_terms_to_nullify.txt")

    @classmethod
    def read_sunroof_terms_to_nullify(cls):
        return cls.read_file_lines_stripped("wordbanks/sunroof_terms_to_nullify.txt")

    @classmethod
    def read_global_blacklist_values(cls):
        return cls.read_file_lines_stripped("wordbanks/global_blacklist_values.txt")

    @classmethod
    def read_global_blacklist_values_to_nullify(cls):
        return cls.read_file_lines_stripped("wordbanks/global_blacklist_values_to_nullify.txt")

    @classmethod
    def read_is_awd_terms(cls):
        return cls.read_file_lines_stripped("wordbanks/is_awd_terms.txt")

    @classmethod
    def read_awd_terms_to_nullify(cls):
        return cls.read_file_lines_stripped("wordbanks/awd_terms_to_nullify.txt")

    @classmethod
    def read_subaru_mispellings(cls):
        return cls.read_file_lines_stripped("wordbanks/subaru_mispellings.txt")

    @classmethod
    def read_subaru_models(cls):
        return cls.read_file_lines_stripped("wordbanks/subaru_models.txt")

    @classmethod
    def read_subaru_models_mispellings_intodict(cls):
        lines_stripped = cls.read_file_lines_stripped("wordbanks/subaru_models_mispellings.txt")
        return cls.get_model_mispellings_data_from_lines_stripped(lines_stripped)

    @classmethod
    def print_file_data(cls, lines_stripped, filename):
        print "[+] Showing lines parsed from file: %s" % filename
        for line in lines_stripped:
            print line

    @classmethod
    def get_model_mispellings_data_from_lines_stripped(cls, lines_stripped):
        data = {}
        for line in lines_stripped:
            line_split = line.split(",")
            if len(line_split) == 1:
                data[line_split[0]] = ""
            elif len(line_split) == 2:
                data[line_split[0]] = line_split[1]
            else:
                print "[+] Condition in file_reader not being tested in line 105"

        return data

    @classmethod
    def read_subaru_series(cls):
        return cls.read_file_lines_stripped("wordbanks/subaru_series.txt")

    @classmethod
    def read_chevrolet_models(cls):
        return cls.read_file_lines_stripped("wordbanks/chevrolet_models.txt")

    @classmethod
    def read_chevrolet_series(cls):
        return cls.read_file_lines_stripped("wordbanks/chevrolet_series.txt")

    @classmethod
    def read_chevrolet_models_toskip(cls):
        return cls.read_file_lines_stripped("wordbanks/chevrolet_models_toskip.txt")

    @classmethod
    def read_chevrolet_series_toskip(cls):
        return cls.read_file_lines_stripped("wordbanks/chevrolet_series_toskip.txt")

    @classmethod
    def read_ford_models(cls):
        return cls.read_file_lines_stripped("wordbanks/ford_models.txt")

    @classmethod
    def read_ford_series(cls):
        return cls.read_file_lines_stripped("wordbanks/ford_series.txt")

    @classmethod
    def read_dodge_models(cls):
        return cls.read_file_lines_stripped("wordbanks/dodge_models.txt")

    @classmethod
    def read_dodge_series(cls):
        return cls.read_file_lines_stripped("wordbanks/dodge_series.txt")

    @classmethod
    def read_vauto_js(cls):
        pass

    @classmethod
    def read_gmc_series(cls):
        return cls.read_file_lines_stripped("wordbanks/gmc_series.txt")

    @classmethod
    def read_gmc_models(cls):
        return cls.read_file_lines_stripped("wordbanks/gmc_models.txt")

    @classmethod
    def read_subaru_series_toskip(cls):
        return cls.read_file_lines_stripped("wordbanks/subaru_series_toskip.txt")















