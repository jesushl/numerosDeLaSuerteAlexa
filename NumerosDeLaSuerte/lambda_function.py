from Loteria                    import loteria

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)

from ask_sdk_core.utils         import is_request_type, is_intent_name
from ask_sdk_model.ui           import SimpleCard
from ask_sdk_model              import Response

from alexa import data, util

sb = SkillBuilder()


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]
        logger.info("handler atributes : {}".format(_))

        speech = _(data.WELCOME_MESSAGE).format(
            _(data.SKILL_NAME), item)
        reprompt = _(data.WELCOME_REPROMPT)

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response


class SorteoIntentIntentHandler(AbstractRequestHandler):
    """Handler for Recipe Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SorteoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SorteoIntentHandler")

        try:
            sorteoName = handler_input.request_envelope.request.intent.slots[
                "sorteoName"].value.lower()
        except AttributeError:
            logger.info("Could not resolve item name")
            sorteoName = None

        loteria = loteria()
        if sorteoName:
            lokyNumbers = loeria.sorteoNumbers(sorteoName)
            card_title = data.DISPLAY_CARD_TITLE.format(
                data.SKILL_NAME, sorteoName)
            handler_input.response_builder.speak(lokyNumbers).set_card(
                    SimpleCard(card_title, lokyNumbers))
        else:
            card_title = data.DISPLAY_CARD_TITLE.format(
                data.SKILL_NAME, '')
            handler_input.response_builder.speak(lokyNumbers).set_card(
                    SimpleCard(card_title, lokyNumbers))

        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        handler_input.response_builder.speak(data.HELP_MESSAGE).ask(data.HELP_MESSAGE)
        return handler_input.response_builder.response




class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Handler for Cancel and Stop Intents."""
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")
        speech = data.STOP_MESSAGE
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response



sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SorteoIntentIntentHandler())
sb.add_request_handler(HelpIntentHandler())

sb.add_request_handler(CancelOrStopIntentHandler())






lambda_handler = sb.lambda_handler()
