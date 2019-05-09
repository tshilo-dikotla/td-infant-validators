from edc_constants.constants import YES, OTHER
from edc_form_validators import FormValidator


class KaraboTBHistoryFormValidator(FormValidator):

    def clean(self):

        self.required_if(
            YES,
            field='coughing',
            field_required='coughing_rel'
        )

        self.validate_other_specify(
            field='coughing_rel',
            other_specify_field='other_coughing_rel',
            other_stored_value=OTHER)

        self.required_if(
            YES,
            field='fever',
            field_required='fever_rel'
        )

        self.validate_other_specify(
            field='fever_rel',
            other_specify_field='other_fever_rel',
            other_stored_value=OTHER)

        self.required_if(
            YES,
            field='weight_loss',
            field_required='weight_loss_rel'
        )

        self.validate_other_specify(
            field='weight_loss_rel',
            other_specify_field='other_weight_loss',
            other_stored_value=OTHER)

        self.required_if(
            YES,
            field='night_sweats',
            field_required='night_sweats_rel'
        )

        self.validate_other_specify(
            field='night_sweats_rel',
            other_specify_field='other_night_sweats',
            other_stored_value=OTHER)

        self.required_if(
            YES,
            field='diagnosis',
            field_required='diagnosis_rel'
        )

        self.validate_other_specify(
            field='diagnosis_rel',
            other_specify_field='other_diagnosis_rel',
            other_stored_value=OTHER)

        self.required_if(
            YES,
            field='tb_exposure',
            field_required='tb_exposure_det'
        )
