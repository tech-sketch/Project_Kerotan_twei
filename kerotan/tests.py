from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template import RequestContext

from .views import display_google_map
from .forms import AddressForm


# Create your tests here.
class UrlResolveTests(TestCase):
    def test_url_resolves_to_display_google_maps(self):
        found = resolve("/")
        self.assertEqual(found.func, display_google_map)


# ----------------------------------------------------------------------------------------------------------------------
class HtmlTestBase(TestCase):
    def prepare_for_testing(self, method_name):
        self.request = HttpRequest()
        self.request.method = method_name
        self.request.form = AddressForm()

    def check_StatusCode200(self, response, expected_html):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_html.status_code,200)

    def check_ContentEqual(self, response, expected_html):
        self.assertEqual(response.content.decode(), expected_html.content.decode())


# ----------------------------------------------------------------------------------------------------------------------
class HtmlTests_GET(HtmlTestBase):
    # リクエストに対して、正しいレスポンスを返すかどうか
    def test_display_google_maps_page_returns_correct_html(self):
        # GETリクエストに対して、
        # レスポンス：render_to_response('kerotan/test_Gmap.html', {'form':form}, RequestContext(request))
        # を返すことのテスト
        request = HttpRequest()
        request.method = "GET"
        request.form = AddressForm()
        response = display_google_map(request)

        form = AddressForm()
        expected_html = render_to_response('kerotan/test_Gmap.html', {'form': form}, RequestContext(request))
        # print("response", response)
        # print("expected_html", expected_html)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_html.status_code,200)
        self.assertEqual(response.content.decode(), expected_html.content.decode())


# ----------------------------------------------------------------------------------------------------------------------
class HtmlTests_POST(HtmlTestBase):
    def test_display_google_maps_page_returns_correct_html(self):
        # POSTリクエストに対して、
        # レスポンス：render_to_response('kerotan/test_Gmap.html', {'form':form}, RequestContext(request))
        # を返すことのテスト
        # super(HtmlTests_POST, self).prepare_for_testing("POST")
        # HtmlTestBase.prepare_for_testing(self, method_name="POST")
        self.prepare_for_testing("POST")

        self._test_POST_with_noFormData(self.request)

        self._test_POST_with_invalidInput(self.request)
        self._test_POST_with_invalidInput2(self.request)
        self._test_POST_with_invalidInput3(self.request)

    def _test_POST_with_noFormData(self, request):
        response = display_google_map(request)

        expected_html = render_to_response('kerotan/test_Gmap.html', {'form': AddressForm()}, RequestContext(request))

        self.check_StatusCode200(response=response, expected_html=expected_html)
        self.check_ContentEqual(response=response, expected_html=expected_html)

    def _test_POST_with_invalidInput(self, request):
        request.form.start_address = ""
        request.form.arriv_address = ""
        response = display_google_map(request)

        expected_html = render_to_response('kerotan/test_Gmap.html', {'form': AddressForm()}, RequestContext(request))

        self.check_StatusCode200(response, expected_html)
        self.check_ContentEqual(response, expected_html)

    def _test_POST_with_invalidInput2(self, request):
        request.form.start_address = "まヴぉｗしえｊｆｂはｎ"
        request.form.arriv_address = "：；：＊＊もかｚ、ｍｄｚもしあじぇうぃふぉあねｗｃな"
        response = display_google_map(request)

        expected_html = render_to_response('kerotan/test_Gmap.html', {'form': AddressForm()}, RequestContext(request))

        self.check_StatusCode200(response, expected_html)
        self.check_ContentEqual(response, expected_html)

    def _test_POST_with_invalidInput3(self, request):
        request.form.start_address = ""
        request.form.arriv_address = "：；：＊＊もかｚ、ｍｄｚもしあじぇうぃふぉあねｗｃな"
        response = display_google_map(request)

        expected_html = render_to_response('kerotan/test_Gmap.html', {'form': AddressForm()}, RequestContext(request))

        self.check_StatusCode200(response, expected_html)
        self.check_ContentEqual(response, expected_html)

        print("res", response.content.decode())
        print("----------------------------------------------------")
        print("res", expected_html.content.decode())
        self.assertEqual(response.content.decode(), expected_html.content.decode())


# class geocodeViewTest(TestCase):

    # def test_response_with_invalid_input(self):
    # 	invalid_input_view = display_google_map
    # 	invalid_input_view.start_company="aaa"
    # 	invalid_input_view.arriv_company="bbb"
    # 	# invalid_input = AddressForm(start_address="aaa", arriv_address="bbb")
    # 	# url = reverse('/', args=(form.start_address="日本", form.arriv_address='日本'))
    # 	url = reverse('/', args=(invalid_input_view))
    # 	response = self.client.post(url)
    # 	self.assertEqual(response.status_code, 404)