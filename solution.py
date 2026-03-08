import json
from typing import List


class Solution:
    expected_freq = {
        36: 164,
        18: 84,
        9: 48,
        1: 1
    }

    def __init__(self, data_file_path: str, protocol_json_path: str):
        self.data_file_path = data_file_path
        self.protocol_json_path = protocol_json_path
        with open(protocol_json_path, 'r') as json_file:
            self.protocol_json = json.load(json_file)

    # Question 1: What is the version name used in the communication session?
    def q1(self) -> str:
        with open(self.data_file_path, 'r') as f:
            first_line = f.readline()
            hexa_version = first_line.split(',')[-1]
            return bytes.fromhex(hexa_version).decode('ascii')

    # Question 2: Which protocols have wrong messages frequency in the session compared to their expected frequency based on FPS?
    def q2(self) -> List[str]:
        msg_count = self._msg_count()
        wrong_freq = []
        protocols = self.protocol_json["protocols"]
        for prot, count in msg_count.items():
            if count != self.expected_freq[int(protocols[prot.strip()]["fps"])]:
                wrong_freq.append(prot.strip())
        return wrong_freq

    # Question 3: Which protocols are listed as relevant for the version but are missing in the data file?
    def q3(self) -> List[str]:
        not_listed = []
        msg_count = self._msg_count()
        version = self.q1()
        id_type = self.protocol_json["protocols_by_version"][version]["id_type"]
        protocols = self.protocol_json["protocols_by_version"][version]["protocols"]
        for prot in protocols:
            prot = str(hex(int(prot))) if id_type == "dec" else prot
            if prot not in msg_count:
                not_listed.append(prot)
        return not_listed

    # Question 4: Which protocols appear in the data file but are not listed as relevant for the version?
    def q4(self) -> List[str]:
        not_listed = []
        msg_count = self._msg_count()
        version = self.q1()
        id_type = self.protocol_json["protocols_by_version"][version]["id_type"]
        # convert to set for fast search
        protocols = set(self.protocol_json["protocols_by_version"][version]["protocols"])
        for prot in msg_count.keys():
            org_prot = prot
            prot = str(int(prot, 16)) if id_type == "dec" else prot
            if prot not in protocols:
                not_listed.append(org_prot)
        return not_listed

    # Question 5: Which protocols have at least one message in the session with mismatch between the expected size integer and the actual message content size?
    def q5(self) -> List[str]:
        mismatched_protocols = set()  # no duplications
        with open(self.data_file_path, 'r') as f:
            lines = f.readlines()
            for line_str in lines:
                line = line_str.split(',')
                expected = line[3].split(' ')[1]
                msg_length = len(line[4].strip().split(' '))
                if int(expected) != msg_length:
                    mismatched_protocols.add(line[2].strip())
        return list(mismatched_protocols)

    # Question 6: Which protocols are marked as non dynamic_size in protocol.json, but appear with inconsistent expected message sizes Integer in the data file?
    def q6(self) -> List[str]:
        has_dynamic_size = self._has_different_expected_size()
        protocols = self.protocol_json["protocols"]
        ans = []
        for prot in has_dynamic_size:
            if not protocols[prot]["dynamic_size"]:
                ans.append(prot)
        return ans

    def _msg_count(self):
        msg_count = {}  # counter
        with open(self.data_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                prot_id = line.split(',')[2].strip()
                if prot_id not in msg_count:
                    msg_count[prot_id] = 1
                else:
                    msg_count[prot_id] += 1
        return msg_count

    def _has_different_expected_size(self):
        prot_msg_size = {}
        ans = set()
        with open(self.data_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line_list = line.split(',')
                prot = line_list[2].strip()
                expected_size = line_list[3].split(' ')[1]
                if prot not in prot_msg_size:
                    prot_msg_size[prot] = expected_size
                elif prot_msg_size[prot] != expected_size:
                    ans.add(prot)
            return list(ans)


if __name__ == '__main__':
    sol = Solution("data.txt", "protocol.json")
    print(sol.q6())