from rest_framework import serializers
from candidates.models import Candidate


class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    
    def validate_status(self, status_update):
        '''
        Will validate data for status to ensure
        that status can only move between 
        pending and either accepted or rejected,
        but not between accepted and rejected.

        Will then check if the candidate has been
        reviewed and set it to True if it has not.
        '''
        if self.instance:
            if self.instance.status != Candidate.PENDING and status_update in (Candidate.ACCEPTED, Candidate.REJECTED):
                raise serializers.ValidationError('Status cannot go between Accepted and Rejected')
            elif not self.instance.reviewed:
                self.instance.reviewed = True
            return status_update
        return status_update

    class Meta:
        model = Candidate
        fields = ('id', 'name', 'years_exp', 'status', 'date_applied', 'reviewed', 'description', 'created', 'updated')
        read_only_fields = ('id', 'created')