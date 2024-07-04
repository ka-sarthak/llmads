from pydantic import BaseModel, Field


class XRDSettings(BaseModel):
    """
    A data model class that contains the settings for X-ray diffraction.
    """

    xray_tube_material: str = Field(description='Type of the X-ray tube')
    xray_tube_current: float = Field(description='Current of the X-ray tube')
    xray_tube_current_unit: str = Field(description='Unit of the X-ray tube current')
    xray_tube_voltage: float = Field(description='Voltage of the X-ray tube')
    xray_tube_voltage_unit: str = Field(description='Unit of the X-ray tube voltage')
    kalpha_one: float = Field(description='Wavelength of the Kα1 line')
    kalpha_one_unit: str = Field(description='Unit of the Kα1 wavelength')
    kalpha_two: float = Field(description='Wavelength of the Kα2 line')
    kalpha_two_unit: str = Field(description='Unit of the Kα2 wavelength')
    ratio_kalphatwo_kalphaone: float = Field(description='Kα2/Kα1 intensity ratio')
    kbeta: float = Field(description='Wavelength of the Kβ line')
    kbeta_unit: str = Field(description='Unit of the Kβ wavelength')


class XRDResult(BaseModel):
    """
    A data model class that contains the result of X-ray diffraction.
    """

    intensity: list[float] = Field(description='A long list of intensity count values.')
    two_theta: list[float] = Field(description='The start and end of two_theta values.')
    two_theta_step: float = Field(description='The step size of two_theta values.')
    omega: list[float] = Field(
        description='The start and end of omega value (or single value).'
    )
    omega_step: float = Field(description='The step size of omega values.')
    phi: list[float] = Field(
        description='The start and end of phi value (or single value).'
    )
    phi_step: float = Field(description='The step size of phi values.')
    chi: list[float] = Field(
        description='The start and end of chi value (or single value).'
    )
    chi_step: float = Field(description='The step size of chi values.')
    source_peak_wavelength: float = Field(description='Wavelength of the X-ray source.')


class XRayDiffraction(BaseModel):
    """
    A data model class that contains the settings and result of X-ray diffraction.
    """

    settings: XRDSettings
    result: XRDResult
