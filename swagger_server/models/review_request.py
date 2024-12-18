# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ReviewRequest(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, rating: int=None):  # noqa: E501
        """ReviewRequest - a model defined in Swagger

        :param rating: The rating of this ReviewRequest.  # noqa: E501
        :type rating: int
        """
        self.swagger_types = {
            'rating': int
        }

        self.attribute_map = {
            'rating': 'rating'
        }
        self._rating = rating

    @classmethod
    def from_dict(cls, dikt) -> 'ReviewRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ReviewRequest of this ReviewRequest.  # noqa: E501
        :rtype: ReviewRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def rating(self) -> int:
        """Gets the rating of this ReviewRequest.

        Rating for the content (1 to 5 stars)  # noqa: E501

        :return: The rating of this ReviewRequest.
        :rtype: int
        """
        return self._rating

    @rating.setter
    def rating(self, rating: int):
        """Sets the rating of this ReviewRequest.

        Rating for the content (1 to 5 stars)  # noqa: E501

        :param rating: The rating of this ReviewRequest.
        :type rating: int
        """
        if rating is None:
            raise ValueError("Invalid value for `rating`, must not be `None`")  # noqa: E501

        self._rating = rating
