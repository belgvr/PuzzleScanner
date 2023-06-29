import subprocess
import bitcoin
import random
import time
import sys
import argparse

# Define argument parser
parser = argparse.ArgumentParser(description="Solve bitcoin puzzles.")
parser.add_argument("-p", type=int, help="Puzzle ID to attempt")
parser.add_argument("-m", type=int, choices=[0, 1], default=0, help="Scan mode: 0 for random, 1 for incremental")
args = parser.parse_args()

# Create a dictionary of puzzles
puzzles = {
    1: {"LOWER": "1", "UPPER": "1", "WALLET": "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"},
    2: {"LOWER": "2", "UPPER": "3", "WALLET": "1CUNEBjYrCn2y1SdiUMohaKUi4wpP326Lb"},
    3: {"LOWER": "4", "UPPER": "7", "WALLET": "19ZewH8Kk1PDbSNdJ97FP4EiCjTRaZMZQA"},
    4: {"LOWER": "8", "UPPER": "f", "WALLET": "1EhqbyUMvvs7BfL8goY6qcPbD6YKfPqb7e"},
    5: {"LOWER": "10", "UPPER": "1f", "WALLET": "1E6NuFjCi27W5zoXg8TRdcSRq84zJeBW3k"},
    6: {"LOWER": "20", "UPPER": "3f", "WALLET": "1PitScNLyp2HCygzadCh7FveTnfmpPbfp8"},
    7: {"LOWER": "40", "UPPER": "7f", "WALLET": "1McVt1vMtCC7yn5b9wgX1833yCcLXzueeC"},
    8: {"LOWER": "80", "UPPER": "ff", "WALLET": "1M92tSqNmQLYw33fuBvjmeadirh1ysMBxK"},
    9: {"LOWER": "100", "UPPER": "1ff", "WALLET": "1CQFwcjw1dwhtkVWBttNLDtqL7ivBonGPV"},
    10: {"LOWER": "200", "UPPER": "3ff", "WALLET": "1LeBZP5QCwwgXRtmVUvTVrraqPUokyLHqe"},
    11: {"LOWER": "400", "UPPER": "7ff", "WALLET": "1PgQVLmst3Z314JrQn5TNiys8Hc38TcXJu"},
    12: {"LOWER": "800", "UPPER": "fff", "WALLET": "1DBaumZxUkM4qMQRt2LVWyFJq5kDtSZQot"},
    13: {"LOWER": "1000", "UPPER": "1fff", "WALLET": "1Pie8JkxBT6MGPz9Nvi3fsPkr2D8q3GBc1"},
    14: {"LOWER": "2000", "UPPER": "3fff", "WALLET": "1ErZWg5cFCe4Vw5BzgfzB74VNLaXEiEkhk"},
    15: {"LOWER": "4000", "UPPER": "7fff", "WALLET": "1QCbW9HWnwQWiQqVo5exhAnmfqKRrCRsvW"},
    16: {"LOWER": "8000", "UPPER": "ffff", "WALLET": "1BDyrQ6WoF8VN3g9SAS1iKZcPzFfnDVieY"},
    17: {"LOWER": "10000", "UPPER": "1ffff", "WALLET": "1HduPEXZRdG26SUT5Yk83mLkPyjnZuJ7Bm"},
    18: {"LOWER": "20000", "UPPER": "3ffff", "WALLET": "1GnNTmTVLZiqQfLbAdp9DVdicEnB5GoERE"},
    19: {"LOWER": "40000", "UPPER": "7ffff", "WALLET": "1NWmZRpHH4XSPwsW6dsS3nrNWfL1yrJj4w"},
    20: {"LOWER": "80000", "UPPER": "fffff", "WALLET": "1HsMJxNiV7TLxmoF6uJNkydxPFDog4NQum"},
    21: {"LOWER": "100000", "UPPER": "1fffff", "WALLET": "14oFNXucftsHiUMY8uctg6N487riuyXs4h"},
    22: {"LOWER": "200000", "UPPER": "3fffff", "WALLET": "1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv"},
    23: {"LOWER": "400000", "UPPER": "7fffff", "WALLET": "1L2GM8eE7mJWLdo3HZS6su1832NX2txaac"},
    24: {"LOWER": "800000", "UPPER": "ffffff", "WALLET": "1rSnXMr63jdCuegJFuidJqWxUPV7AtUf7 "},
    25: {"LOWER": "1000000", "UPPER": "1ffffff", "WALLET": "15JhYXn6Mx3oF4Y7PcTAv2wVVAuCFFQNiP"},
    26: {"LOWER": "2000000", "UPPER": "3ffffff", "WALLET": "1JVnST957hGztonaWK6FougdtjxzHzRMMg"},
    27: {"LOWER": "4000000", "UPPER": "7ffffff", "WALLET": "128z5d7nN7PkCuX5qoA4Ys6pmxUYnEy86k"},
    28: {"LOWER": "8000000", "UPPER": "fffffff", "WALLET": "12jbtzBb54r97TCwW3G1gCFoumpckRAPdY"},
    29: {"LOWER": "10000000", "UPPER": "1fffffff", "WALLET": "19EEC52krRUK1RkUAEZmQdjTyHT7Gp1TYT"},
    30: {"LOWER": "20000000", "UPPER": "3fffffff", "WALLET": "1LHtnpd8nU5VHEMkG2TMYYNUjjLc992bps"},
    31: {"LOWER": "40000000", "UPPER": "7fffffff", "WALLET": "1LhE6sCTuGae42Axu1L1ZB7L96yi9irEBE"},
    32: {"LOWER": "80000000", "UPPER": "ffffffff", "WALLET": "1FRoHA9xewq7DjrZ1psWJVeTer8gHRqEvR"},
    33: {"LOWER": "100000000", "UPPER": "1ffffffff", "WALLET": "187swFMjz1G54ycVU56B7jZFHFTNVQFDiu"},
    34: {"LOWER": "200000000", "UPPER": "3ffffffff", "WALLET": "1PWABE7oUahG2AFFQhhvViQovnCr4rEv7Q"},
    35: {"LOWER": "400000000", "UPPER": "7ffffffff", "WALLET": "1PWCx5fovoEaoBowAvF5k91m2Xat9bMgwb"},
    36: {"LOWER": "800000000", "UPPER": "fffffffff", "WALLET": "1Be2UF9NLfyLFbtm3TCbmuocc9N1Kduci1"},
    37: {"LOWER": "1000000000", "UPPER": "1fffffffff", "WALLET": "14iXhn8bGajVWegZHJ18vJLHhntcpL4dex"},
    38: {"LOWER": "2000000000", "UPPER": "3fffffffff", "WALLET": "1HBtApAFA9B2YZw3G2YKSMCtb3dVnjuNe2"},
    39: {"LOWER": "4000000000", "UPPER": "7fffffffff", "WALLET": "122AJhKLEfkFBaGAd84pLp1kfE7xK3GdT8"},
    40: {"LOWER": "8000000000", "UPPER": "ffffffffff", "WALLET": "1EeAxcprB2PpCnr34VfZdFrkUWuxyiNEFv"},
    41: {"LOWER": "10000000000", "UPPER": "1ffffffffff", "WALLET": "1L5sU9qvJeuwQUdt4y1eiLmquFxKjtHr3E"},
    42: {"LOWER": "20000000000", "UPPER": "3ffffffffff", "WALLET": "1E32GPWgDyeyQac4aJxm9HVoLrrEYPnM4N"},
    43: {"LOWER": "40000000000", "UPPER": "7ffffffffff", "WALLET": "1PiFuqGpG8yGM5v6rNHWS3TjsG6awgEGA1"},
    44: {"LOWER": "80000000000", "UPPER": "fffffffffff", "WALLET": "1CkR2uS7LmFwc3T2jV8C1BhWb5mQaoxedF"},
    45: {"LOWER": "100000000000", "UPPER": "1fffffffffff", "WALLET": "1NtiLNGegHWE3Mp9g2JPkgx6wUg4TW7bbk"},
    46: {"LOWER": "200000000000", "UPPER": "3fffffffffff", "WALLET": "1F3JRMWudBaj48EhwcHDdpeuy2jwACNxjP"},
    47: {"LOWER": "400000000000", "UPPER": "7fffffffffff", "WALLET": "1Pd8VvT49sHKsmqrQiP61RsVwmXCZ6ay7Z"},
    48: {"LOWER": "800000000000", "UPPER": "ffffffffffff", "WALLET": "1DFYhaB2J9q1LLZJWKTnscPWos9VBqDHzv"},
    49: {"LOWER": "1000000000000", "UPPER": "1ffffffffffff", "WALLET": "12CiUhYVTTH33w3SPUBqcpMoqnApAV4WCF"},
    50: {"LOWER": "2000000000000", "UPPER": "3ffffffffffff", "WALLET": "1MEzite4ReNuWaL5Ds17ePKt2dCxWEofwk"},
    51: {"LOWER": "4000000000000", "UPPER": "7ffffffffffff", "WALLET": "1NpnQyZ7x24ud82b7WiRNvPm6N8bqGQnaS"},
    52: {"LOWER": "8000000000000", "UPPER": "fffffffffffff", "WALLET": "15z9c9sVpu6fwNiK7dMAFgMYSK4GqsGZim"},
    53: {"LOWER": "10000000000000", "UPPER": "1fffffffffffff", "WALLET": "15K1YKJMiJ4fpesTVUcByoz334rHmknxmT"},
    54: {"LOWER": "20000000000000", "UPPER": "3fffffffffffff", "WALLET": "1KYUv7nSvXx4642TKeuC2SNdTk326uUpFy"},
    55: {"LOWER": "40000000000000", "UPPER": "7fffffffffffff", "WALLET": "1LzhS3k3e9Ub8i2W1V8xQFdB8n2MYCHPCa"},
    56: {"LOWER": "80000000000000", "UPPER": "ffffffffffffff", "WALLET": "17aPYR1m6pVAacXg1PTDDU7XafvK1dxvhi"},
    57: {"LOWER": "100000000000000", "UPPER": "1ffffffffffffff", "WALLET": "15c9mPGLku1HuW9LRtBf4jcHVpBUt8txKz"},
    58: {"LOWER": "200000000000000", "UPPER": "3ffffffffffffff", "WALLET": "1Dn8NF8qDyyfHMktmuoQLGyjWmZXgvosXf"},
    59: {"LOWER": "400000000000000", "UPPER": "7ffffffffffffff", "WALLET": "1HAX2n9Uruu9YDt4cqRgYcvtGvZj1rbUyt"},
    60: {"LOWER": "800000000000000", "UPPER": "fffffffffffffff", "WALLET": "1Kn5h2qpgw9mWE5jKpk8PP4qvvJ1QVy8su"},
    61: {"LOWER": "1000000000000000", "UPPER": "1fffffffffffffff", "WALLET": "1AVJKwzs9AskraJLGHAZPiaZcrpDr1U6AB"},
    62: {"LOWER": "2000000000000000", "UPPER": "3fffffffffffffff", "WALLET": "1Me6EfpwZK5kQziBwBfvLiHjaPGxCKLoJi"},
    63: {"LOWER": "4000000000000000", "UPPER": "7fffffffffffffff", "WALLET": "1NpYjtLira16LfGbGwZJ5JbDPh3ai9bjf4"},
    64: {"LOWER": "8000000000000000", "UPPER": "ffffffffffffffff", "WALLET": "16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN"},
    65: {"LOWER": "10000000000000000", "UPPER": "1ffffffffffffffff", "WALLET": "18ZMbwUFLMHoZBbfpCjUJQTCMCbktshgpe"},
    66: {"LOWER": "20000000000000000", "UPPER": "3ffffffffffffffff", "WALLET": "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"},
    67: {"LOWER": "40000000000000000", "UPPER": "7ffffffffffffffff", "WALLET": "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"},
    68: {"LOWER": "80000000000000000", "UPPER": "fffffffffffffffff", "WALLET": "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ"},
    69: {"LOWER": "100000000000000000", "UPPER": "1fffffffffffffffff", "WALLET": "19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG"},
    70: {"LOWER": "200000000000000000", "UPPER": "3fffffffffffffffff", "WALLET": "19YZECXj3SxEZMoUeJ1yiPsw8xANe7M7QR"},
    71: {"LOWER": "400000000000000000", "UPPER": "7fffffffffffffffff", "WALLET": "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU"},
    72: {"LOWER": "800000000000000000", "UPPER": "ffffffffffffffffff", "WALLET": "1JTK7s9YVYywfm5XUH7RNhHJH1LshCaRFR"},
    73: {"LOWER": "1000000000000000000", "UPPER": "1ffffffffffffffffff", "WALLET": "12VVRNPi4SJqUTsp6FmqDqY5sGosDtysn4"},
    74: {"LOWER": "2000000000000000000", "UPPER": "3ffffffffffffffffff", "WALLET": "1FWGcVDK3JGzCC3WtkYetULPszMaK2Jksv"},
    75: {"LOWER": "4000000000000000000", "UPPER": "7ffffffffffffffffff", "WALLET": "1J36UjUByGroXcCvmj13U6uwaVv9caEeAt"},
    76: {"LOWER": "8000000000000000000", "UPPER": "fffffffffffffffffff", "WALLET": "1DJh2eHFYQfACPmrvpyWc8MSTYKh7w9eRF"},
    77: {"LOWER": "10000000000000000000", "UPPER": "1fffffffffffffffffff", "WALLET": "1Bxk4CQdqL9p22JEtDfdXMsng1XacifUtE"},
    78: {"LOWER": "20000000000000000000", "UPPER": "3fffffffffffffffffff", "WALLET": "15qF6X51huDjqTmF9BJgxXdt1xcj46Jmhb"},
    79: {"LOWER": "40000000000000000000", "UPPER": "7fffffffffffffffffff", "WALLET": "1ARk8HWJMn8js8tQmGUJeQHjSE7KRkn2t8"},
    80: {"LOWER": "80000000000000000000", "UPPER": "ffffffffffffffffffff", "WALLET": "1BCf6rHUW6m3iH2ptsvnjgLruAiPQQepLe"},
    81: {"LOWER": "100000000000000000000", "UPPER": "1ffffffffffffffffffff", "WALLET": "15qsCm78whspNQFydGJQk5rexzxTQopnHZ"},
    82: {"LOWER": "200000000000000000000", "UPPER": "3ffffffffffffffffffff", "WALLET": "13zYrYhhJxp6Ui1VV7pqa5WDhNWM45ARAC"},
    83: {"LOWER": "400000000000000000000", "UPPER": "7ffffffffffffffffffff", "WALLET": "14MdEb4eFcT3MVG5sPFG4jGLuHJSnt1Dk2"},
    84: {"LOWER": "800000000000000000000", "UPPER": "fffffffffffffffffffff", "WALLET": "1CMq3SvFcVEcpLMuuH8PUcNiqsK1oicG2D"},
    85: {"LOWER": "1000000000000000000000", "UPPER": "1fffffffffffffffffffff", "WALLET": "1Kh22PvXERd2xpTQk3ur6pPEqFeckCJfAr"},
    86: {"LOWER": "2000000000000000000000", "UPPER": "3fffffffffffffffffffff", "WALLET": "1K3x5L6G57Y494fDqBfrojD28UJv4s5JcK"},
    87: {"LOWER": "4000000000000000000000", "UPPER": "7fffffffffffffffffffff", "WALLET": "1PxH3K1Shdjb7gSEoTX7UPDZ6SH4qGPrvq"},
    88: {"LOWER": "8000000000000000000000", "UPPER": "ffffffffffffffffffffff", "WALLET": "16AbnZjZZipwHMkYKBSfswGWKDmXHjEpSf"},
    89: {"LOWER": "10000000000000000000000", "UPPER": "1ffffffffffffffffffffff", "WALLET": "19QciEHbGVNY4hrhfKXmcBBCrJSBZ6TaVt"},
    90: {"LOWER": "20000000000000000000000", "UPPER": "3ffffffffffffffffffffff", "WALLET": "1L12FHH2FHjvTviyanuiFVfmzCy46RRATU"},
    91: {"LOWER": "40000000000000000000000", "UPPER": "7ffffffffffffffffffffff", "WALLET": "1EzVHtmbN4fs4MiNk3ppEnKKhsmXYJ4s74"},
    92: {"LOWER": "80000000000000000000000", "UPPER": "fffffffffffffffffffffff", "WALLET": "1AE8NzzgKE7Yhz7BWtAcAAxiFMbPo82NB5"},
    93: {"LOWER": "100000000000000000000000", "UPPER": "1fffffffffffffffffffffff", "WALLET": "17Q7tuG2JwFFU9rXVj3uZqRtioH3mx2Jad"},
    94: {"LOWER": "200000000000000000000000", "UPPER": "3fffffffffffffffffffffff", "WALLET": "1K6xGMUbs6ZTXBnhw1pippqwK6wjBWtNpL"},
    95: {"LOWER": "400000000000000000000000", "UPPER": "7fffffffffffffffffffffff", "WALLET": "19eVSDuizydXxhohGh8Ki9WY9KsHdSwoQC"},
    96: {"LOWER": "800000000000000000000000", "UPPER": "ffffffffffffffffffffffff", "WALLET": "15ANYzzCp5BFHcCnVFzXqyibpzgPLWaD8b"},
    97: {"LOWER": "1000000000000000000000000", "UPPER": "1ffffffffffffffffffffffff", "WALLET": "18ywPwj39nGjqBrQJSzZVq2izR12MDpDr8"},
    98: {"LOWER": "2000000000000000000000000", "UPPER": "3ffffffffffffffffffffffff", "WALLET": "1CaBVPrwUxbQYYswu32w7Mj4HR4maNoJSX"},
    99: {"LOWER": "4000000000000000000000000", "UPPER": "7ffffffffffffffffffffffff", "WALLET": "1JWnE6p6UN7ZJBN7TtcbNDoRcjFtuDWoNL"},
    100: {"LOWER": "8000000000000000000000000", "UPPER": "fffffffffffffffffffffffff", "WALLET": "1KCgMv8fo2TPBpddVi9jqmMmcne9uSNJ5F"},
    101: {"LOWER": "10000000000000000000000000", "UPPER": "1fffffffffffffffffffffffff", "WALLET": "1CKCVdbDJasYmhswB6HKZHEAnNaDpK7W4n"},
    102: {"LOWER": "20000000000000000000000000", "UPPER": "3fffffffffffffffffffffffff", "WALLET": "1PXv28YxmYMaB8zxrKeZBW8dt2HK7RkRPX"},
    103: {"LOWER": "40000000000000000000000000", "UPPER": "7fffffffffffffffffffffffff", "WALLET": "1AcAmB6jmtU6AiEcXkmiNE9TNVPsj9DULf"},
    104: {"LOWER": "80000000000000000000000000", "UPPER": "ffffffffffffffffffffffffff", "WALLET": "1EQJvpsmhazYCcKX5Au6AZmZKRnzarMVZu"},
    105: {"LOWER": "100000000000000000000000000", "UPPER": "1ffffffffffffffffffffffffff", "WALLET": "1CMjscKB3QW7SDyQ4c3C3DEUHiHRhiZVib"},
    106: {"LOWER": "200000000000000000000000000", "UPPER": "3ffffffffffffffffffffffffff", "WALLET": "18KsfuHuzQaBTNLASyj15hy4LuqPUo1FNB"},
    107: {"LOWER": "400000000000000000000000000", "UPPER": "7ffffffffffffffffffffffffff", "WALLET": "15EJFC5ZTs9nhsdvSUeBXjLAuYq3SWaxTc"},
    108: {"LOWER": "800000000000000000000000000", "UPPER": "fffffffffffffffffffffffffff", "WALLET": "1HB1iKUqeffnVsvQsbpC6dNi1XKbyNuqao"},
    109: {"LOWER": "1000000000000000000000000000", "UPPER": "1fffffffffffffffffffffffffff", "WALLET": "1GvgAXVCbA8FBjXfWiAms4ytFeJcKsoyhL"},
    110: {"LOWER": "2000000000000000000000000000", "UPPER": "3fffffffffffffffffffffffffff", "WALLET": "12JzYkkN76xkwvcPT6AWKZtGX6w2LAgsJg"},
    111: {"LOWER": "4000000000000000000000000000", "UPPER": "7fffffffffffffffffffffffffff", "WALLET": "1824ZJQ7nKJ9QFTRBqn7z7dHV5EGpzUpH3"},
    112: {"LOWER": "8000000000000000000000000000", "UPPER": "ffffffffffffffffffffffffffff", "WALLET": "18A7NA9FTsnJxWgkoFfPAFbQzuQxpRtCos"},
    113: {"LOWER": "10000000000000000000000000000", "UPPER": "1ffffffffffffffffffffffffffff", "WALLET": "1NeGn21dUDDeqFQ63xb2SpgUuXuBLA4WT4"},
    114: {"LOWER": "20000000000000000000000000000", "UPPER": "3ffffffffffffffffffffffffffff", "WALLET": "174SNxfqpdMGYy5YQcfLbSTK3MRNZEePoy"},
    115: {"LOWER": "40000000000000000000000000000", "UPPER": "7ffffffffffffffffffffffffffff", "WALLET": "1NLbHuJebVwUZ1XqDjsAyfTRUPwDQbemfv"},
    116: {"LOWER": "80000000000000000000000000000", "UPPER": "fffffffffffffffffffffffffffff", "WALLET": "1MnJ6hdhvK37VLmqcdEwqC3iFxyWH2PHUV"},
    117: {"LOWER": "100000000000000000000000000000", "UPPER": "1fffffffffffffffffffffffffffff", "WALLET": "1KNRfGWw7Q9Rmwsc6NT5zsdvEb9M2Wkj5Z"},
    118: {"LOWER": "200000000000000000000000000000", "UPPER": "3fffffffffffffffffffffffffffff", "WALLET": "1PJZPzvGX19a7twf5HyD2VvNiPdHLzm9F6"},
    119: {"LOWER": "400000000000000000000000000000", "UPPER": "7fffffffffffffffffffffffffffff", "WALLET": "1GuBBhf61rnvRe4K8zu8vdQB3kHzwFqSy7"},
    120: {"LOWER": "800000000000000000000000000000", "UPPER": "ffffffffffffffffffffffffffffff", "WALLET": "17s2b9ksz5y7abUm92cHwG8jEPCzK3dLnT"},
    121: {"LOWER": "1000000000000000000000000000000", "UPPER": "1ffffffffffffffffffffffffffffff", "WALLET": "1GDSuiThEV64c166LUFC9uDcVdGjqkxKyh"},
    122: {"LOWER": "2000000000000000000000000000000", "UPPER": "3ffffffffffffffffffffffffffffff", "WALLET": "1Me3ASYt5JCTAK2XaC32RMeH34PdprrfDx"},
    123: {"LOWER": "4000000000000000000000000000000", "UPPER": "7ffffffffffffffffffffffffffffff", "WALLET": "1CdufMQL892A69KXgv6UNBD17ywWqYpKut"},
    124: {"LOWER": "8000000000000000000000000000000", "UPPER": "fffffffffffffffffffffffffffffff", "WALLET": "1BkkGsX9ZM6iwL3zbqs7HWBV7SvosR6m8N"},
    125: {"LOWER": "10000000000000000000000000000000", "UPPER": "1fffffffffffffffffffffffffffffff", "WALLET": "1PXAyUB8ZoH3WD8n5zoAthYjN15yN5CVq5"},
    126: {"LOWER": "20000000000000000000000000000000", "UPPER": "3fffffffffffffffffffffffffffffff", "WALLET": "1AWCLZAjKbV1P7AHvaPNCKiB7ZWVDMxFiz"},
    127: {"LOWER": "40000000000000000000000000000000", "UPPER": "7fffffffffffffffffffffffffffffff", "WALLET": "1G6EFyBRU86sThN3SSt3GrHu1sA7w7nzi4"},
    128: {"LOWER": "80000000000000000000000000000000", "UPPER": "ffffffffffffffffffffffffffffffff", "WALLET": "1MZ2L1gFrCtkkn6DnTT2e4PFUTHw9gNwaj"},
    129: {"LOWER": "100000000000000000000000000000000", "UPPER": "1ffffffffffffffffffffffffffffffff", "WALLET": "1Hz3uv3nNZzBVMXLGadCucgjiCs5W9vaGz"},
    130: {"LOWER": "200000000000000000000000000000000", "UPPER": "3ffffffffffffffffffffffffffffffff", "WALLET": "1Fo65aKq8s8iquMt6weF1rku1moWVEd5Ua"},
    131: {"LOWER": "400000000000000000000000000000000", "UPPER": "7ffffffffffffffffvffffffffffffffff", "WALLET": "16zRPnT8znwq42q7XeMkZUhb1bKqgRogyy"},
    132: {"LOWER": "800000000000000000000000000000000", "UPPER": "fffffffffffffffffffffffffffffffff", "WALLET": "1KrU4dHE5WrW8rhWDsTRjR21r8t3dsrS3R"},
    133: {"LOWER": "1000000000000000000000000000000000", "UPPER": "1fffffffffffffffffffffffffffffffff", "WALLET": "17uDfp5r4n441xkgLFmhNoSW1KWp6xVLD "},
    134: {"LOWER": "2000000000000000000000000000000000", "UPPER": "3fffffffffffffffffffffffffffffffff", "WALLET": "13A3JrvXmvg5w9XGvyyR4JEJqiLz8ZySY3"},
    135: {"LOWER": "4000000000000000000000000000000000", "UPPER": "7fffffffffffffffffffffffffffffffff", "WALLET": "16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v"},
    136: {"LOWER": "8000000000000000000000000000000000", "UPPER": "ffffffffffffffffffffffffffffffffff", "WALLET": "1UDHPdovvR985NrWSkdWQDEQ1xuRiTALq "},
    137: {"LOWER": "10000000000000000000000000000000000", "UPPER": "1ffffffffffffffffffffffffffffffffff", "WALLET": "15nf31J46iLuK1ZkTnqHo7WgN5cARFK3RA"},
    138: {"LOWER": "20000000000000000000000000000000000", "UPPER": "3ffffffffffffffffffffffffffffffffff", "WALLET": "1Ab4vzG6wEQBDNQM1B2bvUz4fqXXdFk2WT"},
    139: {"LOWER": "40000000000000000000000000000000000", "UPPER": "7ffffffffffffffffffffffffffffffffff", "WALLET": "1Fz63c775VV9fNyj25d9Xfw3YHE6sKCxbt"},
    140: {"LOWER": "80000000000000000000000000000000000", "UPPER": "fffffffffffffffffffffffffffffffffff", "WALLET": "1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo"},
    141: {"LOWER": "100000000000000000000000000000000000", "UPPER": "1fffffffffffffffffffffffffffffffffff", "WALLET": "1CD91Vm97mLQvXhrnoMChhJx4TP9MaQkJo"},
    142: {"LOWER": "200000000000000000000000000000000000", "UPPER": "3fffffffffffffffffffffffffffffffffff", "WALLET": "15MnK2jXPqTMURX4xC3h4mAZxyCcaWWEDD"},
    143: {"LOWER": "400000000000000000000000000000000000", "UPPER": "7fffffffffffffffffffffffffffffffffff", "WALLET": "13N66gCzWWHEZBxhVxG18P8wyjEWF9Yoi1"},
    144: {"LOWER": "800000000000000000000000000000000000", "UPPER": "ffffffffffffffffffffffffffffffffffff", "WALLET": "1NevxKDYuDcCh1ZMMi6ftmWwGrZKC6j7Ux"},
    145: {"LOWER": "1000000000000000000000000000000000000", "UPPER": "1ffffffffffffffffffffffffffffffffffff", "WALLET": "19GpszRNUej5yYqxXoLnbZWKew3KdVLkXg"},
    146: {"LOWER": "2000000000000000000000000000000000000", "UPPER": "3ffffffffffffffffffffffffffffffffffff", "WALLET": "1M7ipcdYHey2Y5RZM34MBbpugghmjaV89P"},
    147: {"LOWER": "4000000000000000000000000000000000000", "UPPER": "7ffffffffffffffffffffffffffffffffffff", "WALLET": "18aNhurEAJsw6BAgtANpexk5ob1aGTwSeL"},
    148: {"LOWER": "8000000000000000000000000000000000000", "UPPER": "fffffffffffffffffffffffffffffffffffff", "WALLET": "1FwZXt6EpRT7Fkndzv6K4b4DFoT4trbMrV"},
    149: {"LOWER": "10000000000000000000000000000000000000", "UPPER": "1fffffffffffffffffffffffffffffffffffff", "WALLET": "1CXvTzR6qv8wJ7eprzUKeWxyGcHwDYP1i2"},
    150: {"LOWER": "20000000000000000000000000000000000000", "UPPER": "3fffffffffffffffffffffffffffffffffffff", "WALLET": "1MUJSJYtGPVGkBCTqGspnxyHahpt5Te8jy"},
    151: {"LOWER": "40000000000000000000000000000000000000", "UPPER": "7fffffffffffffffffffffffffffffffffffff", "WALLET": "13Q84TNNvgcL3HJiqQPvyBb9m4hxjS3jkV"},
    152: {"LOWER": "80000000000000000000000000000000000000", "UPPER": "ffffffffffffffffffffffffffffffffffffff", "WALLET": "1LuUHyrQr8PKSvbcY1v1PiuGuqFjWpDumN"},
    153: {"LOWER": "100000000000000000000000000000000000000", "UPPER": "1ffffffffffffffffffffffffffffffffffffff", "WALLET": "18192XpzzdDi2K11QVHR7td2HcPS6Qs5vg"},
    154: {"LOWER": "200000000000000000000000000000000000000", "UPPER": "3ffffffffffffffffffffffffffffffffffffff", "WALLET": "1NgVmsCCJaKLzGyKLFJfVequnFW9ZvnMLN"},
    155: {"LOWER": "400000000000000000000000000000000000000", "UPPER": "7ffffffffffffffffffffffffffffffffffffff", "WALLET": "1AoeP37TmHdFh8uN72fu9AqgtLrUwcv2wJ"},
    156: {"LOWER": "800000000000000000000000000000000000000", "UPPER": "fffffffffffffffffffffffffffffffffffffff", "WALLET": "1FTpAbQa4h8trvhQXjXnmNhqdiGBd1oraE"},
    157: {"LOWER": "1000000000000000000000000000000000000000", "UPPER": "1fffffffffffffffffffffffffffffffffffffff", "WALLET": "14JHoRAdmJg3XR4RjMDh6Wed6ft6hzbQe9"},
    158: {"LOWER": "2000000000000000000000000000000000000000", "UPPER": "3fffffffffffffffffffffffffffffffffffffff", "WALLET": "19z6waranEf8CcP8FqNgdwUe1QRxvUNKBG"},
    159: {"LOWER": "4000000000000000000000000000000000000000", "UPPER": "7fffffffffffffffffffffffffffffffffffffff", "WALLET": "14u4nA5sugaswb6SZgn5av2vuChdMnD9E5"},
    160: {"LOWER": "8000000000000000000000000000000000000000", "UPPER": "ffffffffffffffffffffffffffffffffffffffff", "WALLET": "1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv"},
}

# Get the puzzle ID and scan mode from command line arguments
puzzle_id = args.p
scan_mode = args.m

# Retrieve the selected puzzle's details
puzzle_details = puzzles[puzzle_id]

# Specify lower and upper limits and target address
lower_limit = int(puzzle_details['LOWER'], 16)  # Lower limit in hexadecimal, converted to decimal
upper_limit = int(puzzle_details['UPPER'], 16)  # Upper limit in hexadecimal, converted to decimal
target_address = puzzle_details['WALLET']  # Bitcoin wallet address

# Display target address, range from, and range to
print("Target Address: ", target_address)
print("Range From: ", hex(lower_limit)[2:])
print("Range To: ", hex(upper_limit)[2:])

checked_addresses = 0  # Counter for checked addresses

if scan_mode == 0:  # Random scanning
    while True:
        random_hex = hex(random.randint(lower_limit, upper_limit))[2:].zfill(64)

        private_key = bitcoin.decode_privkey(random_hex, 'hex')
        public_key = bitcoin.privkey_to_pubkey(private_key)

        compressed_public_key = bitcoin.compress(public_key)
        bitcoin_address = bitcoin.pubkey_to_address(compressed_public_key)

        checked_addresses += 1  # Increment the counter for each checked address

        # Update the status line with scan progress
        status_line = f"Checked Addresses: {checked_addresses} - Current Hex: {random_hex}"
        sys.stdout.write(status_line)
        sys.stdout.flush()
        sys.stdout.write('\r')

        if bitcoin_address == target_address:
            print("\n****************************************")
            print("MATCH FOUND!")
            print("Private Key: ", random_hex)
            print("Bitcoin Address (Compressed): ", bitcoin_address)
            print("****************************************\n")

            # Write the output to a file
            filename = f"FOUND_{target_address}.txt"
            with open(filename, "w") as file:
                file.write("MATCH FOUND!\n")
                file.write("Private Key: " + random_hex + "\n")
                file.write("Bitcoin Address (Compressed): " + bitcoin_address + "\n")
                file.write("Number of Checked Addresses: " + str(checked_addresses) + "\n")

            break

elif scan_mode == 1:  # Incremental scanning
    for i in range(lower_limit, upper_limit + 1):
        random_hex = hex(i)[2:].zfill(64)

        private_key = bitcoin.decode_privkey(random_hex, 'hex')
        public_key = bitcoin.privkey_to_pubkey(private_key)

        compressed_public_key = bitcoin.compress(public_key)
        bitcoin_address = bitcoin.pubkey_to_address(compressed_public_key)

        checked_addresses += 1  # Increment the counter for each checked address

        # Update the status line with scan progress
        status_line = f"Checked Addresses: {checked_addresses} - Current Hex: {random_hex}"
        sys.stdout.write(status_line)
        sys.stdout.flush()
        sys.stdout.write('\r')

        if bitcoin_address == target_address:
            print("\n****************************************")
            print("MATCH FOUND!")
            print("Private Key: ", random_hex)
            print("Bitcoin Address (Compressed): ", bitcoin_address)
            print("****************************************\n")

            # Write the output to a file
            filename = f"FOUND_{target_address}.txt"
            with open(filename, "w") as file:
                file.write("MATCH FOUND!\n")
                file.write("Private Key: " + random_hex + "\n")
                file.write("Bitcoin Address (Compressed): " + bitcoin_address + "\n")
                file.write("Number of Checked Addresses: " + str(checked_addresses) + "\n")

            break

print("\nEnd of program")
