import json
import operator

from modules.exceptions import MissConfigurationError


class SchemaValidation(object):

    _schema = {
       "jobs": {
            "attributes": {
                "type": dict
            }
        },
        "fields": {
            "execute": {
                "attributes": {
                    "type": list,
                    "nullable": True,
                    "required_fields": [
                        "shell"
                    ]
                    "non_required_fields": [
                        "sudo"
                    ]
                }
            },
            "dirs": {
                "attributes": {
                    "type": list,
                    "nullable": False,
                    "required_fields": [
                        "destination",
                        "metadata"
                    ]
                },
                "destination": {
                    "attributes": {
                        "nullable": False,
                        "type": str
                    }
                },
                "metadata": {
                    "attributes": {
                        "nullable": False,
                        "type": dict,
                        "required_fields": [
                            "owner",
                            "group",
                            "chmod",
                            "sudo"
                        ],
                        "non_required_fields": [
                            "notify_after",
                            "notify_before"
                        ]
                    }
                }    
            }
        }
        #    "services",
        #    "env_vars",
        #    "templates",
        #    "before_install",
        #    "after_install",
        #    "test",
        #    "execute",
        #    "install",
        #    "remove_install"
    }

    def __init__(self, obj):
        self.jobs = obj

    def check_types(self):
        if type(self.jobs["jobs"]) != self._schema["jobs"]["attributes"]["type"]:
            raise MissConfigurationError("Check your configuration key 'jobs' must be preset and it must be a dict type")

        try:

            for k,v in self.jobs["jobs"].items():
                if type(self.jobs[k]) != self._schema["fields"][k]["attributes"]["type"]:
                    raise MissConfigurationError("Check your configuration key '{}' must be preset and it must be a {} type".format(
                        k, self._schema["fields"][k]["type"]
                        )
                    )

        # Temp till finish schema implementations
        except KeyError as e:
            print(str(e))



        for field,value in self.jobs["jobs"].items():
            try:
                func = getattr(self, field)
                func(value)

            # Temp till finish schema implementations
            except AttributeError as e:
                print(str(e))

    def execute(self, attributes):
        pass

    def templates(self, attributes):
        pass

    def dirs(self, attributes):
        keys_to_validate = []
        keys_list = []

        # Check for nullables

        keys = list(self._schema["fields"]["dirs"].keys())
        keys.remove("attributes")

        for k in keys:
            if not self._schema["fields"]["dirs"][k]["attributes"]["nullable"]:
                keys_list.append(k)


        for k in attributes:
            # Checking default fields
            keys_to_validate = list(k.keys())
            keys_not_present = [i for i in keys_to_validate if not i in keys_list]
            keys_must_present = [i for i in keys_list if i not in keys_to_validate]

            if keys_not_present:
                raise MissConfigurationError("Was found key(s) not allowed at your config: {}".format(
                    ",".join(keys_not_present)
                    )
                )

            if keys_must_present:
                raise MissConfigurationError("There are nullable fields you must set: {}".format(
                    ",".join(keys_must_present)
                    )
                )

            # Checking metadata fields
            keys_list = self._schema["fields"]["dirs"]["metadata"]["attributes"]["required_fields"]
            keys_to_validate = list(k["metadata"].keys())
            keys_not_present = [i for i in keys_to_validate if not i in keys_list]
            keys_must_present = [i for i in keys_list if i not in keys_to_validate]

            if keys_not_present:
                raise MissConfigurationError("Was found key(s) not allowed at your metadata config: {}".format(
                    ",".join(keys_not_present)
                    )
                )

            if keys_must_present:
                raise MissConfigurationError("There are nullable fields you must set at your metadata: {}".format(
                    ",".join(keys_must_present)
                    )
                )
