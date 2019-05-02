from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantCongenitalAnomaliesFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='cns')


class InfantFacialDefectFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='facial_defect',
            other_specify_field='facial_defects_other')


class InfantCleftDisorderFormFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='cleft_disorder',
            other_specify_field='cleft_disorders_other')


class InfantMouthUpGiFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='mouth_up_gi')


class InfantCardioDisorderFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='cardio_disorder',
            other_specify_field='cardiovascular_other')


class InfantRespiratoryDefectFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='respiratory_defect',
            other_specify_field='respiratory_defects_other')


class InfantLowerGiFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='lower_gi')


class InfantFemaleGenitalFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='female_genital')


class InfantMaleGenitalFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='male_genital')


class InfantRenalFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='renal')


class InfantMusculoskeletalFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='musculo_skeletal')


class InfantSkinFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='skin')


class InfantTrisomiesFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_other_specify(
            field='trisomies')


class InfantCnsFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
