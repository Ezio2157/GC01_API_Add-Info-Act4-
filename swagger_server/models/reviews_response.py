# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.reviews_response_reviews import ReviewsResponseReviews  # noqa: F401,E501
from swagger_server import util


class ReviewsResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, reviews: List[ReviewsResponseReviews]=None):  # noqa: E501
        """ReviewsResponse - a model defined in Swagger

        :param reviews: The reviews of this ReviewsResponse.  # noqa: E501
        :type reviews: List[ReviewsResponseReviews]
        """
        self.swagger_types = {
            'reviews': List[ReviewsResponseReviews]
        }

        self.attribute_map = {
            'reviews': 'reviews'
        }
        self._reviews = reviews

    @classmethod
    def from_dict(cls, dikt) -> 'ReviewsResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ReviewsResponse of this ReviewsResponse.  # noqa: E501
        :rtype: ReviewsResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def reviews(self) -> List[ReviewsResponseReviews]:
        """Gets the reviews of this ReviewsResponse.


        :return: The reviews of this ReviewsResponse.
        :rtype: List[ReviewsResponseReviews]
        """
        return self._reviews

    @reviews.setter
    def reviews(self, reviews: List[ReviewsResponseReviews]):
        """Sets the reviews of this ReviewsResponse.


        :param reviews: The reviews of this ReviewsResponse.
        :type reviews: List[ReviewsResponseReviews]
        """

        self._reviews = reviews